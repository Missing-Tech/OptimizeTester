# pip install pytransloadit
# pip install python-decouple
from fileinput import filename
import pathlib
from transloadit import client
from decouple import config
import csv

# Create a .env file with these values for your account
AUTH_KEY = config('AUTH_KEY')
AUTH_SECRET = config('AUTH_SECRET')

tl = client.Transloadit(AUTH_KEY, AUTH_SECRET)

qualities = {25, 50, 75, 100}
images = {
    'test0.webp', 
    'test1.jpg', 
    'test2.jpg', 
    'test3.png', 
    'test4.png', 
    'test5.jpg',
    'test6.jpg',
    'test7.gif',
    'test8.svg',
    'test9.gif',
    'test10.webp',
    'test10.svg',
}
FILENAME = 'quality.csv'

# Write columns of CSV
with open(FILENAME, mode='w') as columns:
    column_writer = csv.writer(
        columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    column_writer.writerow(['Image', 'Input Size (MB)', 'Output Size (MB)', 'Execution Time (s)',
                            'Input Format', 'Output Format',  'Quality'])


def write_to_csv(image, quality, assembly_response):
    print(assembly_response.data)
    input_size = assembly_response.data['uploads'][0]['size'] / 1000000
    output_size = assembly_response.data['results']['format'][0]['size'] / 1000000
    execution_time = assembly_response.data['execution_duration']
    input_format = pathlib.Path(image).suffix
    output_format = assembly_response.data['results']['format'][0]['ext']

    with open(FILENAME, mode='a') as data:
        data_writer = csv.writer(
            data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([image, input_size, output_size, execution_time, input_format,
                              output_format, quality])


count = 0
for image in images:
    for quality in qualities:
        assembly = tl.new_assembly()

        # Set Encoding Instructions
        assembly.add_step('format', '/image/resize', {
            'use': ':original',
            'format': 'jpg',
            'quality': quality
        })

        # Add files to upload
        assembly.add_file(open(image, 'rb'))

        # Start the Assembly
        assembly_response = assembly.create(retries=5, wait=True)

        write_to_csv(image, quality, assembly_response)
        count += 1
        print(count)
