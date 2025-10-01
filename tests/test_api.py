import pytest
import tempfile
import os
from pathlib import Path
from talenWF import FindTALTask



class TestFindTALTask:
    """Test the FindTALTask class."""
    
    @pytest.fixture
    def sample_fasta_file(self):
        """Create a temporary FASTA file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
            f.write(">test_10400_T\n")
            f.write(f"{'T'*20 + 'C'*21 + 'A'*20}\n")
            temp_file = f.name
        yield temp_file
        os.unlink(temp_file)
    
    @pytest.fixture
    def output_file(self):
        """Create a temporary output file path."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        yield temp_file
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    def test_find_tal_task_basic(self, sample_fasta_file, output_file):
        """Test basic functionality of FindTALTask."""
        # Create FindTALTask instance
        task = FindTALTask(
            fasta=sample_fasta_file,
            min_spacer=14,
            max_spacer=18,
            array_min=14,
            array_max=18,
            outpath=output_file,
            filter_base=31,
        )
        
        # Run the task
        df = task.run()
        
        # Check that DataFrame was returned
        assert df is not None
        assert len(df) > 0
        
        # Check that output file was created
        assert os.path.exists(output_file)
        
        # Check that output file has content
        with open(output_file, 'r') as f:
            content = f.read()
            assert len(content) > 0
            assert 'Sequence Name' in content
    
    def test_find_tal_task_without_filter(self, sample_fasta_file, output_file):
        """Test FindTALTask without filter_base."""
        task = FindTALTask(
            fasta=sample_fasta_file,
            min_spacer=14,
            max_spacer=18,
            array_min=14,
            array_max=18,
            outpath=output_file,
        )

        
        df = task.run()
        
        assert df is not None
        assert os.path.exists(output_file)

