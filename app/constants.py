# boundaries of similarity
MSE_THRESHOLD = 0.45
SSIM_THRESHOLD = 0.5
VGG16_THRESHOLD = 0.8

# text color coloring of words on the page, GREEN color
FILL_TEXT_COLOR = (0, 255, 0)

# supported archive extension for page download
ARCHIVE_EXPANSION = ('zip', 'rar')

MODEL_FILE_TYPE = (
    ('rar', 'RAR Archive'),
    ('zip', 'ZIP Archive'),
    ('png', 'PNG Image'),
    ('jpeg', 'JPEG Image'),
)

MODEL_COMPARISON_METHOD = (
    ('mse', 'Mean Squared Error (MSE)'),
    ('ssim', 'Structural Similarity Index (SSIM)'),
    ('vgg16', 'Neural Network vvgg VGG16'),
)
