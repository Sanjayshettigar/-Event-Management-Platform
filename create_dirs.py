import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Create necessary directories
base_dir = os.path.dirname(os.path.abspath(__file__))
directories = [
    os.path.join(base_dir, 'app', 'static'),
    os.path.join(base_dir, 'app', 'static', 'css'),
    os.path.join(base_dir, 'app', 'static', 'js'),
    os.path.join(base_dir, 'app', 'static', 'images'),
    os.path.join(base_dir, 'app', 'static', 'uploads'),
    os.path.join(base_dir, 'app', 'templates'),
    os.path.join(base_dir, 'app', 'templates', 'auth'),
    os.path.join(base_dir, 'app', 'templates', 'events'),
    os.path.join(base_dir, 'instance'),
]

for directory in directories:
    create_directory(directory)
    print(f'Created directory: {directory}')
