# import csv
from tags import tags
import inflect
plural = inflect.engine()
import requests
from bs4 import BeautifulSoup
import re
from builtwith import builtwith
from func_timeout import func_timeout
from tags.tags import job_opening_admin, job_opening_analytics, job_opening_engineering, job_opening_IT, job_opening_marketing, job_opening_sales


topics_list = [tags.ai_first, 
              tags.certificates, 
              tags.community, 
              tags.demo, 
              tags.e_commerce,
              tags.event,
              tags.free_plan,
              tags.free_trial,
              tags.generative_ai,
                tags.job_opening,
                tags.news_letter,
                tags.offer, 
                tags.partner,
                tags.plg,
                tags.press_release,
                tags.pricing,
                tags.product_tour,
                tags.video_content,
                tags.webinar]



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






def send_request(url):
    header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    
    header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    filename = 'data/'+ url.replace('https://','').replace('http://','').replace('www.','') + '.html'
    original_url = url
    url = url.lower()
    url = "https://www." +  url.replace("https://", "").replace("http://", "").replace("www.", "")

    try:
        try:
            result =  requests.get(url,headers = header,timeout=50,verify=True)
            soup = BeautifulSoup(result.text,'html.parser')
            # file = open(filename,'w')
            # file.write(result.text)
            # file.close()
            print(result.status_code)
            return [original_url,result,soup]
        
        # retrying if ssl certificate error
        except requests.exceptions.SSLError:
                result =  requests.get(url.replace('https://','http://'),headers = header,timeout=50)
                soup = BeautifulSoup(result.text,'html.parser')
                # file = open(filename,'w')
                # file.write(result.text)
                # file.close()
                print(result.status_code)
                return [original_url,result,soup]
         
        except requests.exceptions.ConnectionError as c:
            return c
        
        except requests.exceptions.Timeout as t:
            return t         
    except Exception as f:
         print(f)
         return "Cant reach website"



def scrape_links(soup):
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

    return set(links)


def generic_email_extractor(soup):
    email_result ={}
    emails = re.findall('\S+@\S+', str(soup.text)) 
    if emails:
        email_result['generic_email'] = True
        email_result['generic_email_available'] = {'email':set(emails)}
    return email_result



def description_extractor(soup):
    description_result = {}
    try:
        meta = soup.find('head').find_all('meta')
        for each in meta:
            if 'name="description"' in str(each):
                each = str(each).replace('name="description','').\
                    replace('meta content="','').\
                        replace('<','').replace('>','').\
                        replace('"',"").replace('/','').lstrip().rstrip()
                
                description_result['description'] ={'description': str(each)[:300]}
                return description_result
    except:
        pass


def social_handle_extractor(urls):
    social_handle_result = {}

    for each_link in urls:
        if 'facebook.com' in each_link:
            # social_handle_result['facebook']= True
            social_handle_result['facebook_url']= each_link

        if 'twitter.com' in each_link:
            # social_handle_result['twitter']= True
            social_handle_result['twitter_url']= each_link

        if 'linkedin.com' in each_link:
            # social_handle_result['linkedin']= True
            social_handle_result['linkedin_url']= each_link

        if 'instagram.com' in each_link:
            # social_handle_result['instagram']= True
            social_handle_result['instagram_url']= each_link

    return social_handle_result



def tag_check(soup,links):
    soup_text = str(soup).lower().replace(' ','')
    topic_dict = topic_dict_create()
    result = {}

    for each_link in links:
        each_link = each_link.replace('.html','')
        if each_link.endswith('/'):
            each_link = each_link[:-1]

        for each_value, each_key in topic_dict.items():
            if each_link[- len(each_value)::] == each_value or \
                        "www." + each_value +'.' in each_link or \
                            "https://" + each_value +'.' in each_link or\
                               "/" + each_value + "/" in each_link:
                
                result[each_key]=True
                result[each_key +'_source']=[{each_value:each_link}]

       
        for each_value, each_key in topic_dict.items():
            
            if re.match('>' + each_value.replace(" ",'').lower() + '<',soup_text):
                if not result.get(each_key):
                    result[each_key]=True
                    result[each_key+'_source']=[{each_value+'>':''}]   
    return result




def built_with(website):
    header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    website = "https://www." +  website.replace("https://", "").replace("http://", "").replace("www.", "")
    return builtwith(website,headers=header)

def tech_stacks(website):
    tech_result = {}
    builtwith(website)
    try:
        tech_result['tech_used'] =   func_timeout(20,built_with,args=(website,)) 
        return tech_result
    except:
        pass




def job_opening_check(job_url):
    result = {}
    response = send_request(job_url)
    response = response[2].find('body').text.lower()

    for each in job_opening_admin:
        if each.lower() in response:
            result ['job_opening_admin'] = True

    for each in job_opening_engineering:
        if each.lower() in response:
            result ['job_opening_engineering'] = True

    for each in job_opening_analytics:
        if each.lower() in response:
            result ['job_opening_analytics'] = True
    
    for each in job_opening_IT:
        if each.lower() in response:
            result ['job_opening_IT'] = True

    for each in job_opening_marketing:
        if each.lower() in response:
            result ['job_opening_marketing'] = True

    for each in job_opening_sales:
        if each.lower() in response:
            result ['job_opening_sales'] = True

    return result







