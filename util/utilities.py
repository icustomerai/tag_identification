# import csv
from tags import tags
import inflect
plural = inflect.engine()
import requests
from bs4 import BeautifulSoup
import re
from func_timeout import func_timeout
from tags.bad_website_tags import bad_websites
from tags.tags import job_opening_admin, job_opening_analytics, job_opening_engg, job_opening_IT, job_opening_marketing, job_opening_sales
from techno_check.tech_in_use import builtwith
# from builtwith import builtwith
import time

''' to convert all tags in a list to search each keyword of each tag on the webpage'''
topics_list = [tags.ai_first, 
              tags.certificate, 
              tags.community, 
              tags.demo, 
              tags.ecommerce,
              tags.event,
              tags.free_plan,
              tags.free_trial,
              tags.generative_ai,
                tags.job_page,
                tags.newsletter,
                tags.offer, 
                tags.partner,
                tags.plg,
                tags.press_release,
                tags.pricing,
                tags.product_tour,
                tags.video_content,
                tags.webinar]




'''to create variations of each tag to search on the webpage.
    i.e "e commerce", "e-commerce","e_commerce","ecommerce"
    or "press-release","press_release","pressrelease" ....
    '''
def topic_dict_create():
  all_topics_keywords = []
  all_topics = []
  topic_dict = {}
  for each_topic in topics_list:
      for each_keyword in each_topic[1:]:
          all_topics.append(each_topic[0][0])
          all_topics_keywords.append(each_keyword.lower())

          all_topics.append(each_topic[0][0])
          all_topics_keywords.append(plural.plural(each_keyword.lower()))

          all_topics.append(each_topic[0][0])
          all_topics_keywords.append(each_keyword.lower().replace(" ","-"))

          all_topics.append(each_topic[0][0])
          all_topics_keywords.append(each_keyword.lower().replace(" ","_"))

          all_topics.append(each_topic[0][0])
          all_topics_keywords.append(each_keyword.lower().replace(" ",""))


  for each_k, each_t in zip(all_topics_keywords,all_topics):
      topic_dict[each_k]=each_t

  return topic_dict




''' to validae if the website is valid or invalid or redirecting.
    invalid websites are based on the keywords list of "bad_websites" which has been found and updated
    after r&d, the websites have these content when they are not live'''
def validate_response(response):

    if response == {'error':'connection error'}:
        return {'validation_status':'connection error'}
    
    if response == {'error': 'timeout error'}:
        return {'validation_status': 'timeout error'}
    
    if response == {'error': 'can not reach website'}:
        return {'validation_status': 'can not reach website'}
    
    original_url = response[0]
    response = response[1]
    
    if 'data-adblockkey=' in response.text.lower():
         return {'validation_status':'invalid website - data-adblockkey'}
    
    if response.status_code == 403:
        return {'validation_status':'forbidden'}

    soup = BeautifulSoup(response.text,'html.parser')

    for each in bad_websites:
            if each.lower() in soup.text.lower():
                remarks = each.title()
                return {'validation_status':f'invalid website - {remarks}'}
    

    # Checking if the website is redirecting, by matching original and received url
    url1 = original_url
    url2 = response.url
    url1 =  str(url1).lower().replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
    url2 =  str(url2).lower().replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
    if url1 not in url2 or url2 not in url1:
        return {'validation_status':'redirecting'}

    response = {'original_url':original_url,
                'response':response,
                'soup_obj':soup,
                'validation_status':'valid'}
    
    return response



# tosending request on the website
def send_request(url):
    # print('sending request ......',url)
    header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    original_url = url
    url = url.lower()
    url = "https://www." +  url.replace("https://", "").replace("http://", "").replace("www.", "")

    try:
        try:
            result =  requests.get(url,headers = header,timeout=10,verify=True)
        
            return [original_url, result]
        
        # retrying if ssl certificate error
        except requests.exceptions.SSLError:
                result =  requests.get(url.replace('https://','http://'),headers = header,timeout=10,verify=False)
                return [original_url, result]
         
        except requests.exceptions.ConnectionError as e:
            return {'error':'connection error'}
        
        except requests.exceptions.Timeout as e:
            return {'error': 'timeout error'}
             
    except Exception as e:
         return {'error': 'can not reach website'}



# to scrape all urls from the website into a set
def links_extractor(soup):
    links = []
    for each in soup.find_all('a'):
        try:
            if each['href'][-1] == "/":
                each = each['href'][:-1]
                links.append(each)
            else:
                links.append(each['href'])
        except:
            pass
    return {'links':list(set(links))}


# to extract generic email from the website
# def generic_email_extractor(soup):
#     email_result ={}
#     emails = re.findall('\S+@\S+', str(soup.text)) 
#     if emails:
#         email_result['generic_email'] = "Yes"
#         email_result['generic_email_available'] = {'email':set(emails)}
#     return email_result


# to extract description from the website
def description_extractor(soup):
    description_result = {}
    try:
        meta = soup.find('head').find_all('meta')
        for each in meta:
            if 'name="description"' in str(each) and '\n' not in str(each) and len(str(each)) > 80:

                each = str(each).replace('name="description','').\
                    replace('meta content="','').\
                        replace('<','').replace('>','').\
                        replace('"',"").replace('/','').lstrip().rstrip()
                
                description_result['description'] = str(each)[:300]
                return description_result
            
        if description_result['description'] is None:
            description_result['description'] = ''
            return description_result
    except:
        description_result['description'] = ''
        return description_result 



# to extract social handle from the website
def social_handle_extractor(urls):
    social_handle_result = {}

    for each_link in urls:
        if 'facebook.com' in each_link:
            # social_handle_result['facebook']= True
            social_handle_result['facebook']= each_link

        if 'twitter.com' in each_link:
            # social_handle_result['twitter']= True
            social_handle_result['twitter']= each_link

        if 'linkedin.com' in each_link:
            # social_handle_result['linkedin']= True
            social_handle_result['linkedin']= each_link

        if 'instagram.com' in each_link:
            # social_handle_result['instagram']= True
            social_handle_result['instagram']= each_link

    if not social_handle_result.get('facebook'):
        social_handle_result['facebook']= ''

    if not social_handle_result.get('twitter'):
        social_handle_result['twitter']= ''
    
    if not social_handle_result.get('linkedin'):
        social_handle_result['linkedin']= ''
    
    if not social_handle_result.get('instagram'):
        social_handle_result['instagram']= ''
        
    return social_handle_result


# to check if any variation of the tag is present on the website
def tag_check(soup,links):
    soup_text = str(soup).lower().replace(' ','')
    topic_dict = topic_dict_create()
    result = {}

    # to clean the url
    for each_link in links:
        each_link = each_link.replace('.html','')
        if each_link.endswith('/'):
            each_link = each_link[:-1]

        # to check if any tag variation endswith in any url extracted from the website
        for each_value, each_key in topic_dict.items():
            if each_link[- len(each_value)::] == each_value or \
                        "www." + each_value +'.' in each_link or \
                            "https://" + each_value +'.' in each_link or\
                               "/" + each_value + "/" in each_link:
                
                # to store in a dict 'Yes' if found and the source url
                result[each_key]="Yes"
                result[each_key +'_source']=[{each_value:each_link}]

        # to check each tag variation in the form >tag< in the webpage html document       
        for each_value, each_key in topic_dict.items():     
            if re.match('>' + each_value.replace(" ",'').lower() + '<',soup_text):
                if not result.get(each_key):
                    result[each_key]= "Yes"
                    result[each_key+'_source']=[{each_value+'>':''}]   
    return result




# to extract the technologies the website is builtwith
# def built_with(website):
#     header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
#     }
#     website = "https://www." +  website.replace("https://", "").replace("http://", "").replace("www.", "")
#     return builtwith(website,headers=header)

# def tech_stacks(website):
#     tech_result = {}
#     try:
#         tech_result['technographic'] =   func_timeout(20,built_with,args=(website,)) 
#         return tech_result
#     except:
#         tech_result['technographic']  = ''
#         return tech_result



def tech_stacks(url,request_object):
    # time.sleep(2)
    tech_result = {}
    try:
        tech_result['technographic'] =   builtwith(url=url,request_obj=request_object) #func_timeout(20,builtwith,args=(url,request_object)) 
        if tech_result['technographic'] == {}:
            tech_result['technographic']  = ''
        return tech_result
    except:
        tech_result['technographic']  = ''
        return tech_result




# to check if the website has certain job openings based on the job keyword match in the body of the career or similar page of the website
def job_opening_check(job_url):
    result = {}
    if 'https://' in job_url:

        response = validate_response(send_request(job_url))
        try:
            response = response['soup_obj'].find('body').text.lower()
        
            for each in job_opening_admin[1:]:
                if each.lower() in response:
                    result ['job_opening_admin'] = "Yes"

            if not result.get('job_opening_admin'):
                result ['job_opening_admin'] = "No"


            for each in job_opening_engg[1:]:
                if each.lower() in response:
                    result ['job_opening_engg'] = "Yes"
            
            if not result.get('job_opening_engg'):
                result ['job_opening_engg'] = "No"


            for each in job_opening_analytics[1:]:
                if each.lower() in response:
                    result ['job_opening_analytics'] = "Yes"
            
            if not result.get('job_opening_analytics'):
                result ['job_opening_analytics'] = "No"
            
            for each in job_opening_IT[1:]:
                if each.lower() in response:
                    result ['job_opening_IT'] = "Yes"

            if not result.get('job_opening_IT'):
                result ['job_opening_IT'] = "No"
            
            for each in job_opening_marketing[1:]:
                if each.lower() in response:
                    result ['job_opening_marketing'] = "Yes"
            
            if not result.get('job_opening_marketing'):
                result ['job_opening_marketing'] = "No"

            for each in job_opening_sales[1:]:
                if each.lower() in response:
                    result ['job_opening_sales'] = "Yes"
            
            if not result.get('job_opening_sales'):
                result ['job_opening_sales'] = "No"

            return result
        except:
            result ['job_opening_admin'] = ""
            result ['job_opening_engg'] = ""
            result ['job_opening_analytics'] = ""
            result ['job_opening_IT'] = ""
            result ['job_opening_marketing'] = ""
            result ['job_opening_sales'] = ""
            return result

    else:
        result ['job_opening_admin'] = ""
        result ['job_opening_engg'] = ""
        result ['job_opening_analytics'] = ""
        result ['job_opening_IT'] = ""
        result ['job_opening_marketing'] = ""
        result ['job_opening_sales'] = ""
        return result







