#!/usr/bin/env python3
"""
Simple script to check if the talenWF package is working correctly.
"""

def check_imports():
    """Check if all imports work correctly."""
    try:
        from talenWF import FindTALTask, RunFindTALTask
        print("✅ Imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def check_basic_functionality():
    """Check basic functionality with a simple test."""
    try:
        from talenWF import FindTALTask
        import tempfile
        import os
        
        # Create a simple test FASTA
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
            f.write(">test_sequence\n")
            f.write("TTTTTTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAAAAA\n")
            temp_fasta = f.name
        
        try:
            # Test FindTALTask
            task = FindTALTask(
                fasta=temp_fasta,
                min_spacer=14,
                max_spacer=18,
                array_min=14,
                array_max=18,
                outpath='NA',  # No output file
                filter_base=31,
            )
            
            df = task.run()
            
            if df is not None and len(df) > 0:
                print("✅ Basic functionality test passed")
                print(f"   Found {len(df)} TAL pairs")
                return True
            else:
                print("❌ Basic functionality test failed - no results")
                return False
                
        finally:
            # Clean up
            if os.path.exists(temp_fasta):
                os.unlink(temp_fasta)
                
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all checks."""
    print("Checking talenWF package...")
    print("=" * 40)
    
    import_ok = check_imports()
    func_ok = check_basic_functionality()
    
    print("=" * 40)
    if import_ok and func_ok:
        print("🎉 All checks passed! Package is working correctly.")
        return 0
    else:
        print("💥 Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
