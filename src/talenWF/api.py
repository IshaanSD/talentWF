from pathlib import Path
from typing import List, Optional
from collections import deque
import pandas as pd
from Bio import SeqIO

COMPLEMENT = {
    'T': 'A',
    'A': 'T',
    'C': 'G',
    'G': 'C'
}

def findAll(seq, sub, start=0, end=None):
    if end is None:
        end = len(seq)
    return [i for i in range(start, end) if seq[i:i+len(sub)] == sub]

class FindTALTask:
    """TALEN window finder class."""
    
    def __init__(
        self,
        fasta: str,
        min_spacer: int = 14,
        max_spacer: int = 18,
        array_min: int = 14,
        array_max: int = 18,
        outpath: str = 'talenWF_out',
        filter_base: Optional[int] = None,
        upstream_bases: List[str] = ['T'],
    ):
        """
        Initialize the TAL window finder.
        
        Args:
            fasta: The FASTA file to process.
            min_spacer: The minimum spacer length.
            max_spacer: The maximum spacer length.
            array_min: The minimum array length.
            array_max: The maximum array length.
            filter_base: The base position to filter. If None, no filtering is done.
            upstream_bases: The upstream bases to consider. (Default: ['T'])
            outpath: The path to the output file.
        """
        self.fasta = fasta
        self.min_spacer = min_spacer
        self.max_spacer = max_spacer
        self.array_min = array_min
        self.array_max = array_max
        self.outpath = outpath
        self.filter_base = filter_base
        self.upstream_bases = upstream_bases
        
        # Calculate distances
        self.max_dist = 2 * array_max + max_spacer  # max dist between TAL1 and TAL2 start/end
        self.min_dist = 2 * array_min + min_spacer  # min dist between TAL1 and TAL2 start/end

    def _find_tal_pairs_for_seq(self):
        """Generator function that yields TAL pairs for a sequence."""
        for upstream_base in self.upstream_bases:
            downstream_base = COMPLEMENT[upstream_base]
            if self.filter_base is not None:
                if self.filter_base - (self.max_dist//2) < 0 or (self.filter_base + ((self.max_dist+1)//2) + 1) > len(self.sequence):
                    continue  # only one cut site is possible
                up_pos_array = findAll(self.sequence, upstream_base, 
                               self.filter_base - (self.max_dist//2) - 1, 
                               self.filter_base - (self.min_dist//2) - 1)
                down_pos_array = findAll(self.sequence, downstream_base, 
                                 self.filter_base + ((self.min_dist+1)//2), 
                                 self.filter_base + ((self.max_dist+1)//2) + 1)

                for up_pos in up_pos_array:
                    for down_pos in down_pos_array:
                        assert self.sequence[up_pos] == upstream_base
                        assert self.sequence[down_pos] == downstream_base
                        for spacer_length in range(self.min_spacer, self.max_spacer + 1):
                            yield self._create_tal_pair(self.filter_base, up_pos, down_pos, spacer_length)
                continue

            upstream_q = deque()
            for j in range(len(self.sequence)):
                ch = self.sequence[j]
                if ch == upstream_base:
                    upstream_q.append(j)
                elif ch == COMPLEMENT[upstream_base]:
                    # remove any Ts that are too old for this A (i < j-max_dist)
                    min_i_allowed = j - self.max_dist
                    while upstream_q and upstream_q[0] < min_i_allowed:
                        upstream_q.popleft()
                    # Ts remaining might start from >= j-max_dist; those <= j-min_dist match
                    max_i_allowed = j - self.min_dist
                    # yield all t in upstream_q with t <= max_i_allowed
                    for t in list(upstream_q):
                        if t <= max_i_allowed:
                            for spacer_length in range(self.min_spacer, self.max_spacer + 1):
                                for cut in range(t + self.min_dist//2, j - self.min_dist//2):
                                    yield self._create_tal_pair(cut, t, j, spacer_length)
                        else:
                            break

    def _create_tal_pair(self, cut: int, up_pos: int, down_pos: int, spacer_length: int):
        """Create a TAL pair attributes dictionary from positions for the output table."""
        tal1_start = up_pos + 1
        tal1_end = cut - spacer_length//2
        tal2_start = cut + (spacer_length+1)//2 -1
        tal2_end = down_pos
            
        tal1 = self.sequence[tal1_start:tal1_end]
        tal2 = self.sequence[tal2_start:tal2_end]
        spacer = self.sequence[tal1_end:tal2_start]
        
        # Compose plus-strand output like legacy tool
        plus_seq = f"{self.sequence[up_pos]} {tal1} {spacer.lower()} {tal2} {self.sequence[down_pos]}"
        return {
            'Sequence Name': self.sequence_id,
            'Cut Site': cut,
            'TAL1 start': tal1_start,
            'TAL2 start': tal2_end-1,
            'TAL1 length': len(tal1),
            'TAL2 length': len(tal2),
            'Spacer length': spacer_length,
            'Spacer range': f"{tal1_end}-{tal2_start}",
            'TAL1 RVDs': '',
            'TAL2 RVDs': '',
            'Plus strand sequence': plus_seq,
            'Unique RE sites in spacer': '',
            '% RVDs HD or NN/NH': '',
        }


    def run(self) -> Optional[pd.DataFrame]:
        """
        Runs the TAL window finder.

        Returns:
            A DataFrame containing the TAL windows.
        """
        # Validate FASTA file exists and is readable
        try:
            with open(self.fasta, 'r') as f:
                # Try to parse the first record to validate FASTA format
                first_record = next(SeqIO.parse(f, 'fasta'))
                logger.info(f"Processing FASTA file: {self.fasta}")
                logger.info(f"First sequence: {first_record.id} (length: {len(first_record.seq)})")
        except FileNotFoundError:
            raise FileNotFoundError(f"FASTA file not found: {self.fasta}")
        except Exception as e:
            raise Exception(f"Error reading FASTA file: {e}")

        tal_window_rows: List[dict] = []
        self.sequence = str(first_record.seq).upper()
        self.sequence_id = first_record.id
        for tal_pair in self._find_tal_pairs_for_seq():
            if tal_pair is not None:
                tal_window_rows.append(tal_pair)

        df = pd.DataFrame(tal_window_rows)
        if self.outpath is not None:
            outpath = Path(self.outpath)
            outpath.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(outpath, sep='\t', index=False)

        return df

