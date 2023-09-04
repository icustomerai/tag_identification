# from util.utilities import topic_dict_create
from tags import tags


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
                # tags.job_opening_admin,
                # tags.job_opening_analytics,
                # tags.job_opening_engg,
                # tags.job_opening_IT,
                # tags.job_opening_marketing,
                # tags.job_opening_sales
                



# these are the values for company type
company_type_columns = ["ai_first",
                        "certificate",
                        "community",
                        "demo",
                        "ecommerce",
                        "event",
                        "free_plan",
                        "free_trial",
                        "generative_ai",
                        "job_opening_admin",
                        "job_opening_analytics",
                        "job_opening_engg",
                        "job_opening_IT",
                        "job_opening_marketing",
                        "job_opening_sales",
                        "job_page",
                        "newsletter",
                        "offer",
                        "partner",
                        "plg",
                        "pricing",
                        "product_tour",
                        "video_content",
                        "webinar",
                        "press_release"
                    ]

technography = ["technographic"]





# to create a list of all dict values of tags
topics = []
for each in topics_list:
    topics.append(each[0][0])

'''this function modifies the response as per our requirement
    currently this is removing datasources, appending value as "No" for all not found tags in company type
    and consolidating all company type tags into a dict
    '''
def response(*args):
    company_type = {}
    final_output = {}

    final_response = {}
    for each in args:
        final_response.update(each)

    source_to_remove = []
    for each in final_response.keys():
        if each.endswith('source'):
            source_to_remove.append(each)

    for each in source_to_remove:
        final_response.pop(each)


    for each in topics:
        if not final_response.get(each):
            final_response[each] = "No"


    for each_key, each_value in final_response.items():
        if each_key in company_type_columns:
            company_type[each_key]= each_value


    final_output["linkedin"] = final_response["linkedin"]
    final_output["instagram"] = final_response["instagram"]
    final_output["twitter"] = final_response["twitter"]
    final_output["facebook"] = final_response["facebook"]
    final_output["description"] = final_response["description"]
    final_output["technographic"] = final_response["technographic"]
    final_output["company_type"] = company_type
    final_output["validation_status"] = final_response["validation_status"]
    final_output["input_domain"] = final_response["input_website"]

    return final_output
