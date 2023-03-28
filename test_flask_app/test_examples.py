# import pytest
# from PIL import Image

# @pytest.fixture
# def reference_image():
#     # Load the reference image
#     return Image.open("reference_image.png")

# @pytest.fixture(params=["test_image1.png", "test_image2.png", "test_image3.png"])
# def test_image(request):
#     # Load the test image
#     return Image.open(request.param)

# def test_image_comparison(reference_image, test_image):
#     # Check that the images have the same dimensions
#     assert reference_image.size == test_image.size
    
#     # Compute the pixel-wise difference between the two images
#     diff_image = ImageChops.difference(reference_image, test_image)
    
#     # Compute the maximum difference between any two pixels
#     max_diff = max(ImageStat.Stat(diff_image).sum)
    
#     # Define a tolerance value for the maximum difference
#     tolerance = 10
    
#     # Check that the maximum difference is below the tolerance level
#     assert max_diff <= tolerance


import pytest
from PIL import Image

@pytest.fixture(params=[("test_image1.png", "test_mask1.png"),
                        ("test_image2.png", "test_mask2.png"),
                        ("test_image3.png", "test_mask3.png")])
def test_image_pair(request):
    # Load the test image and mask
    image = Image.open(request.param[0])
    mask = Image.open(request.param[1])
    
    return (image, mask)

def test_image_mask_comparison(test_image_pair):
    # Unpack the test image and mask
    test_image, test_mask = test_image_pair
    
    # Load the reference image and mask
    reference_image = Image.open("reference_image.png")
    reference_mask = Image.open("reference_mask.png")

    # Check that the images have the same dimensions
    assert reference_image.size == test_image.size
    assert reference_mask.size == test_mask.size
    
    # Compute the pixel-wise difference between the test image and reference image
    diff_image = ImageChops.difference(reference_image, test_image)
    
    # Compute the maximum difference between any two pixels
    max_diff_image = max(ImageStat.Stat(diff_image).sum)
    
    # Compute the pixel-wise difference between the test mask and reference mask
    diff_mask = ImageChops.difference(reference_mask, test_mask)
    
    # Compute the maximum difference between any two pixels
    max_diff_mask = max(ImageStat.Stat(diff_mask).sum)
    
    # Define a tolerance value for the maximum difference
    tolerance = 10
    
    # Check that the maximum differences are below the tolerance level
    assert max_diff_image <= tolerance
    assert max_diff_mask <= tolerance
