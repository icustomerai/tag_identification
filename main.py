from util.utilities import send_request, links_extractor, tag_check, social_handle_extractor, description_extractor,tech_stacks, job_opening_check,validate_response
from response.response import response
import json
import logging
import concurrent.futures
import json

logging.basicConfig(level=logging.INFO,filename='log/log_file.log', encoding='utf-8')

# this is the main functions which calls all the functions from utilites and collects all the responses and does some validation.
def main (website):
    try:
        # sending request on the website
        result = send_request(website)

        # checking if the website is invalid
        result = validate_response(result)


        # if result['validation_status'] != 'valid':
        #     logging.info([website,result['validation_status']])

        # to scrape all links from the website
        try:
            links = links_extractor(result['soup_obj'])
        except Exception as e:
            logging.error([website, e,'ignored'])
            links = {"links":""}

        
        # to scrape social handles, insta, linkedin, facebook, twitter 
        social_handle = social_handle_extractor(links['links'])

        # to scrape description from website meta data

        try:
            description = description_extractor(result['soup_obj'])
        except:
            description = {"description":""}


        # to extract technologies websites is using with builtwith module
        try:
            tech_used =  tech_stacks(website,result['response'])
            # print(tech_used)
        except Exception as e:
            logging.error([website, e,'ignored'])
            tech_used = {'technographic':''}
   
        try:
            # to check all tags present on the website
            topic_result =  tag_check(result["soup_obj"],links["links"])
        except Exception as e:
            logging.error([website, e,'ignored'])
            topic_result = {}
        

        # to store validation status and input original website
        input_website = {"input_website":website}
        validation_status = {"validation_status":result["validation_status"]}


        # if job page is not complete, converting it to complete url. so that the request can be sent to identify if the page has
        # job openings mentioned i.e "/career", "https://www.website.com/career
    
        if topic_result.get("job_page_source"):
            job_url = topic_result.get("job_page_source")
            job_url =  list(job_url[0].values())[0]

            if job_url == 'careers' or job_url == 'career' \
                    or job_url == '/careers' or job_url == '/career' \
                        or job_url =='careers/' or job_url == '/careers/' or job_url == '/career/':
                job_url = 'https://www.' + website.replace('https://','').replace('http://','').replace('wwww.','') +'/' + job_url.replace('/','')
        else:
            job_url = 'nourlfound'
        
        job_opening = job_opening_check(job_url)
    
        # response is the function which collects all the responses and returns in the required format.
        final_response =    response(topic_result,social_handle,description,job_opening,tech_used, validation_status, input_website)

        del result 
        del links 
        del social_handle
        del description 
        del topic_result
        del job_opening
        del tech_used
        del validation_status
        del input_website
        del job_url


        final_response = json.dumps(final_response)
        return final_response
    
    except Exception as e:
        logging.error([website, e])
        input_website = {"input_website":website}
        return input_website
            


# this function calls concurrent multiple instances of main function
def tag_identification(url_list):
    all_urls = []
    for each in url_list:
        all_urls.append(each)
   
    chunk_size = 50
    list_chunks = [all_urls[i:i + chunk_size] for i in range(0, len(all_urls), chunk_size)]

    output = {}
    for each_chunk in list_chunks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            result = executor.map(main, each_chunk)

    
            for each in result: 
                each = json.loads(each)
                try:
                    output[each['input_domain']]=each
                except Exception as e:
                    logging.error((each['input_domain'],e))

    output = json.dumps(output)
    output  = json.loads(output)
    return output

# print(main('denave.com'))

# import pandas as pd
# data = pd.read_csv('input.csv')
# data = data.account_url.to_list()
# from datetime import datetime
# startt = datetime.now()
# x = tag_identification(data)
# pd.read_json(x).transpose().to_csv('testoutput.csv')
# endtime = datetime.now()
# print(startt,endtime)