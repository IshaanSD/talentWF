import argparse
import sys
import logging
from Bio import SeqIO
from .api import FindTALTask

def main():
    """CLI entry point for talenWF."""
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
    logger = logging.getLogger('talenWF')
    parser = argparse.ArgumentParser(description='talenWF: TALEN window finder')
    parser.add_argument('--fasta', required=True, help='FASTA file path')
    parser.add_argument('--min_spacer', type=int, default=14, help='Minimum spacer length for TALE-NT')
    parser.add_argument('--max_spacer', type=int, default=18, help='Maximum spacer length for TALE-NT')
    parser.add_argument('--array_min', type=int, default=14, help='Minimum array length for TALE-NT')
    parser.add_argument('--array_max', type=int, default=18, help='Maximum array length for TALE-NT')
    parser.add_argument('--outpath', default='NA', help='Output path for TALE-NT')
    parser.add_argument('--filter_base', type=int, help='Filter base position for TALE-NT (comma separated)')
    parser.add_argument('--upstream_bases', type=str, help='Upstream bases for TALE-NT (comma separated)')
    args = parser.parse_args()

    # Validate FASTA file exists and is readable
    try:
        with open(args.fasta, 'r') as f:
            # Try to parse the first record to validate FASTA format
            first_record = next(SeqIO.parse(f, 'fasta'))
            logger.info(f"Processing FASTA file: {args.fasta}")
            logger.info(f"First sequence: {first_record.id} (length: {len(first_record.seq)})")
    except FileNotFoundError:
        logger.error(f"FASTA file not found: {args.fasta}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading FASTA file: {e}")
        sys.exit(1)

    # Run the TAL finding task
    logger.info("Starting TAL finding task...")
    FindTALTask(
        fasta=args.fasta,
        min_spacer=args.min_spacer,
        max_spacer=args.max_spacer,
        array_min=args.array_min,
        array_max=args.array_max,
        outpath=args.outpath,
        filter_base=args.filter_base,
        upstream_bases=args.upstream_bases.split(',') if args.upstream_bases else ['T'],
    ).run()
    logger.info("TAL finding task completed successfully!")

if __name__ == '__main__':
    main()


