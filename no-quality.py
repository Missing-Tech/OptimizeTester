# pip install pytransloadit
# pip install python-decouple
from transloadit import client
from decouple import config
import csv

# Create a .env file with these values for your account
AUTH_KEY = config('AUTH_KEY')
AUTH_SECRET = config('AUTH_SECRET')

tl = client.Transloadit(AUTH_KEY, AUTH_SECRET)

priorities = {'conversion-speed', 'compression-ratio'}
booleans = {True, False}
images = {
    'test1.jpg', 
    'test2.jpg', 
    # 'test3.png', 
    # 'test4.png', 
    'test5.jpg',
    'test6.jpg',
    'test7.jpg',
    'test8.jpg',
    'test9.jpg',
    'test10.jpg',
}

# Write columns of CSV
with open('no-quality.csv', mode='w') as columns:
    column_writer = csv.writer(
        columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    column_writer.writerow(['Image', 'Input Size (MB)', 'Output Size (MB)', 'Execution Time (s)',
                            'Input Format', 'Output Format', 'Priority', 'Preserve Meta Data?'])


def write_to_csv(image, priority, is_preserving_meta_data, assembly_response):
    print(assembly_response.data)
    input_size = assembly_response.data['uploads'][0]['size'] / 1000000
    output_size = assembly_response.data['results']['optimize'][0]['size'] / 1000000
    execution_time = assembly_response.data['execution_duration']
    input_format = image[-3:]
    output_format = assembly_response.data['results']['optimize'][0]['ext']

    with open('no-quality.csv', mode='a') as data:
        data_writer = csv.writer(
            data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([image, input_size, output_size, execution_time, input_format,
                              output_format, priority, is_preserving_meta_data])


count = 0
for image in images:
    for priority in priorities:
        for is_preserving_meta_data in booleans:
            assembly = tl.new_assembly()

            # Set Encoding Instructions
            assembly.add_step('optimize', '/image/optimize', {
                'use': ':original',
                'preserve_meta_data': is_preserving_meta_data,
                'priority': priority
            })

            # Add files to upload
            assembly.add_file(open(image, 'rb'))

            # Start the Assembly
            assembly_response = assembly.create(retries=5, wait=True)

            write_to_csv(image, priority, is_preserving_meta_data,
                         assembly_response)
            count += 1
            print(count)
