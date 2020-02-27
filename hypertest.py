import requests
import os
import argparse
import string 
class HyperTest:
    def __init__(self, url):
        self.url = url

        if "https" in self.url:
            self.path = self.url.replace('https://', '')
        elif "http" in self.url:
            self.path = self.url.replace('http://', '')
        try:
            os.mkdir(self.path)
            print('Directory generated')
        except OSError:
            print('Directory already created')
        
    def put_test(self, subdir='put'):
        r = requests.request('PUT', self.url+'/'+subdir, data = 'Put test data')
        return r.text, 'Status Code:'+str(r.status_code), r.headers  

    def delete_test(self, subdir='delete'):
        r = requests.delete(self.url+'/'+subdir)
        return r.text, 'Status Code:'+str(r.status_code), r.headers  

    def head_test(self, subdir='headers'):
        r = requests.head(self.url+'/'+subdir)
        return r.text, 'Status Code:'+str(r.status_code), r.headers 

    def options_test(self, subdir='/'):
        r = requests.options(self.url)
        return r.text, 'Status Code:'+str(r.status_code), r.headers   

    def output_to_file(self, fileName, inputData):
        optionsFile = open(self.path+"/"+fileName+".json", 'w+')
        optionsFile.write(inputData)   

    def default_test(self, subdir='/'):
        print(self.options_test())
        print(self.put_test())
        print(self.delete_test())
        print(self.head_test())
    
    def default_test_output(self):
        self.output_to_file('options', str(self.options_test()))
        self.output_to_file('put',str(self.put_test()))
        self.output_to_file('delete',str(self.delete_test()))
        self.output_to_file('headers',str(self.head_test()))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP/HTTPS Methods Testing')
    parser.add_argument('--url', help='type of test that will be performed', required=True)
    parser.add_argument('--type', help='type of test that will be performed', required=False)
    parser.add_argument('--output', help='Output data to individual files', required=False, action='store_true')
    args = parser.parse_args()
    if args.type is None:
        args.type = 'default'
    testType = args.type
    testType = testType.lower()
    ht = HyperTest(args.url)

    if testType == 'default':
        if args.output:
            ht.default_test_output()
        else:
            ht.default_test()
    if testType == 'put':
        if args.output:
            ht.output_to_file('put', ht.put_test())
        else:
            print(ht.put_test())
    elif testType == 'delete':
        if args.output:
            ht.output_to_file('delete', ht.delete_test())
        else:
            print(ht.delete_test())
    elif testType == 'head':
        if args.output:
            ht.output_to_file('head', ht.head_test())
        else:
            print(ht.head_test())
    elif testType == 'options':
        if args.output:
            ht.output_to_file('options', ht.options_test())
        else:
            print(ht.options_test())

    print('Testing Complete')


