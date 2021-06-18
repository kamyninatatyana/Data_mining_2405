def make_dict(response, css_key, css_value):
    fin_dict = dict(zip(response.css(css_key).extract(), response.css(css_value).extract()))
    return fin_dict

