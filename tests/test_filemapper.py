import tempfile
import json
import os
import sys
from os.path import join, exists, islink

# Add the parent directory to the path so we can import filemapper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from filemapper import process_json_file, parse_data, do_action


json_contents = {
    "{subject}.json": "derivatives/{pipeline}/{subject}-{session}_T1w.json",
    "{subject}.nii.gz": "derivatives/{pipeline}/{subject}-{session}_T1w.nii.gz",
}


def test_simple_mapping():
    # Create temp directory manually so it doesn't auto-cleanup
    outfolder = tempfile.mkdtemp()
    try:
        # Create the JSON template file
        json_file = join(outfolder, "template.json")
        with open(json_file, "w") as outfile:
            json.dump(json_contents, outfile)

        # Create source files that match the template
        source_dir = join(outfolder, "source")
        os.makedirs(source_dir, exist_ok=True)

        # Create test files
        test_files = ["sub-01.json", "sub-01.nii.gz"]
        for filename in test_files:
            with open(join(source_dir, filename), "w") as f:
                f.write("test content")

        # Process the JSON file
        process_json_file(
            json_file=json_file,
            sourcepath=source_dir,
            destpath=join(outfolder, "destination"),
            template="subject=sub-01,pipeline=smooth,session=baseline",
            action="copy",
            testdebug=False,
        )


        # Check if files exist and what type they are
        expected_files = [
            join(
                outfolder,
                "destination",
                "derivatives",
                "smooth",
                "sub-01-baseline_T1w.json",
            ),
            join(
                outfolder,
                "destination",
                "derivatives",
                "smooth",
                "sub-01-baseline_T1w.nii.gz",
            ),
        ]


        # Verify that the destination files were created
        for expected_file in expected_files:
            assert exists(
                expected_file
            ), f"Expected file {expected_file} was not created"

    finally:
        import shutil
        shutil.rmtree(outfolder)


def test_symlink_mapping():
    """Test the filemapper with symlink action to see actual symlinks"""
    # Create temp directory manually so it doesn't auto-cleanup
    outfolder = tempfile.mkdtemp()
    try:
        # Create the JSON template file
        json_file = join(outfolder, "template.json")
        with open(json_file, "w") as outfile:
            json.dump(json_contents, outfile)

        # Create source files that match the template
        source_dir = join(outfolder, "source")
        os.makedirs(source_dir, exist_ok=True)

        # Create test files
        test_files = ["sub-01.json", "sub-01.nii.gz"]
        for filename in test_files:
            with open(join(source_dir, filename), "w") as f:
                f.write("test content")

        # Process the JSON file with SYMLINK action
        process_json_file(
            json_file=json_file,
            sourcepath=source_dir,
            destpath=join(outfolder, "destination"),
            template="subject=sub-01,pipeline=smooth,session=baseline",
            action="symlink",  # This should create symlinks
            testdebug=False,
        )

        expected_files = [
            join(
                outfolder,
                "destination",
                "derivatives",
                "smooth",
                "sub-01-baseline_T1w.json",
            ),
            join(
                outfolder,
                "destination",
                "derivatives",
                "smooth",
                "sub-01-baseline_T1w.nii.gz",
            ),
        ]

        # Verify that the destination files were created
        for expected_file in expected_files:
            assert exists(
                expected_file
            ), f"Expected file {expected_file} was not created"
            assert islink(
                expected_file            
            ), f"Expected file {expected_file} is not a symlink"

    finally:
        # Clean up manually
        import shutil

        shutil.rmtree(outfolder)


def test_parse_data():
    """Test the parse_data function directly"""
    template_dict = {"subject": "sub-01", "pipeline": "smooth", "session": "baseline"}

    # Test template replacement
    result = parse_data(
        json_contents,
        sourcepath=".",
        destpath="destination",
        template="subject=sub-01,pipeline=smooth,session=baseline",
        testdebug=True,
    )

    # The function doesn't return anything, but we can test that it processes without errors
    assert True  # If we get here, no exceptions were raised


def test_do_action_copy():
    """Test the do_action function for copying"""
    # Create temp directory manually so it doesn't auto-cleanup
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a source file
        src_file = join(temp_dir, "source.txt")
        with open(src_file, "w") as f:
            f.write("test content")

        # Define destination
        dest_file = join(temp_dir, "dest.txt")

        # Test copy action
        do_action(
            src_file, dest_file, "copy", testdebug=False
        )  # Set to False to actually perform the operation

        # Verify file was copied
        assert exists(dest_file), "File was not copied"
        with open(dest_file, "r") as f:
            content = f.read()
            assert content == "test content", "File content was not copied correctly"

    finally:
        # Clean up manually
        import shutil

        shutil.rmtree(temp_dir)
