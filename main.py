from util.utilities import send_request, scrape_links, tag_check, social_handle_extractor, description_extractor,generic_email_extractor,tech_stacks, job_opening_check
from response.response import response


def main (website):
    try:
        result = send_request(website)
        links = scrape_links(result[2])
        topic_result =  tag_check(result[2],links)
        topic_result.update({'input_website':website})
        social_handle = social_handle_extractor(links)
        description = description_extractor(result[2])
        generic_emails =  generic_email_extractor(result[2])
        tech_used = tech_stacks(website)
        try:
            job_url = topic_result.get('job_opening_source')
            job_url =  list(job_url[0].values())[0]
            job_opening = job_opening_check(job_url)
        except:
            job_opening = []

        r =    response(topic_result,social_handle,description,generic_emails,job_opening,tech_used)
        return r

    
    except Exception as e:
        # print(e)
        topic_result ={}
        topic_result['input_website'] =  website
        return topic_result
            


# testing
print(main('www.denave.com'))