from bs4 import BeautifulSoup
import json
from .forms import FormWithCaptcha
from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    form = FormWithCaptcha()
    return render(request, 'index.html', context={'form': form})

def fb_video_downloader(request):

    form = FormWithCaptcha()

    if request.method == "POST":



        index = request.POST.get('json_code')

        soup = BeautifulSoup(index, "html.parser")
        script_tags = soup.find_all('script', type='application/json')

        hd_url = ""
        sd_url = ""
        thumb = ""

        hd_urls = []
        sd_urls = []

        success = ''
        warning = ''
        error = ''

        for script_tag in script_tags:
            script_data = script_tag.text
            json_data = json.loads(script_data)
            try:
                if json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['story']['attachments'][0]['media']['browser_native_hd_url'] != None:
                    hd_url = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['story']['attachments'][0]['media']['browser_native_hd_url']
                    thumb = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['story']['attachments'][0]['media']['preferred_thumbnail']['image']['uri']
                else:
                    sd_url = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['story']['attachments'][0]['media']['browser_native_sd_url']
                    thumb = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['story']['attachments'][0]['media']['preferred_thumbnail']['image']['uri']
            except:
                pass


        if hd_url == "" or sd_url == "":
            for script_tag in script_tags:
                script_data = script_tag.text
                json_data = json.loads(script_data)
                try:
                    if json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['browser_native_hd_url'] != None:
                        hd_url = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['browser_native_hd_url']
                        thumb = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['preferred_thumbnail']['image']['uri']
                    else:
                        sd_url = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['browser_native_sd_url']
                        thumb = json_data['require'][0][3][0]['__bbox']['require'][7][3][1]['__bbox']['result']['data']['video']['preferred_thumbnail']['image']['uri']
                except:
                    pass

        if hd_url == "" or sd_url == "":
            for script_tag in script_tags:
                script_data = script_tag.text
                json_data = json.loads(script_data)
                try:
                    stories = len(json_data['require'][0][3][0]['__bbox']['require'][5][3][1]['__bbox']['result']['data']['bucket']['unified_stories']['edges'])
                    if stories > 0:
                        for index in range(stories):
                            data = {
                                'hd_url': json_data['require'][0][3][0]['__bbox']['require'][5][3][1]['__bbox']['result']['data']['bucket']['unified_stories']['edges'][index]['node']['attachments'][0]['media']['browser_native_hd_url'],
                                'thumb': json_data['require'][0][3][0]['__bbox']['require'][5][3][1]['__bbox']['result']['data']['bucket']['unified_stories']['edges'][index]['node']['attachments'][0]['media']['previewImage']['uri']
                            }
                            hd_urls.append(data)
                    else:
                        for index in range(stories):
                            data = {
                                'sd_url': json_data['require'][0][3][0]['__bbox']['require'][5][3][1]['__bbox']['result']['data']['bucket']['unified_stories']['edges'][index]['node']['attachments'][0]['media']['browser_native_hd_url'],
                                'thumb' : json_data['require'][0][3][0]['__bbox']['require'][5][3][1]['__bbox']['result']['data']['bucket']['unified_stories']['edges'][index]['node']['attachments'][0]['media']['previewImage']['uri']
                            }
                            sd_urls.append(data)
                except:
                    pass


        if hd_url == '' and sd_url == '' and len(hd_urls) == 0:
            error = 'Error! Not a video.'
        else:
            success = 'Video downloaded successfully.'
        contex = {
            "hd_url": hd_url,
            "hd_urls": hd_urls,
            "sd_url": sd_url,
            "sd_urls": sd_urls,
            "thumb": thumb,
            "form": form,
            "success": success,
            "error": error,
        }

    return render(request, 'index.html', contex)


# Terms page
def terms(request):
    return render(request, 'terms.html')


# Privacy page
def privacy(request):
    return render(request, 'privacy.html')


# Contact page
def contact(request):
    form = FormWithCaptcha()
    if request.method == "GET":
        return render(request, 'contact.html', context={'form': form})
    else:
        success = ''
        error = ''
        form = FormWithCaptcha()
        try:
            form = FormWithCaptcha(request.POST)
            if form.is_valid():
                name = request.POST.get('name')
                subject = request.POST.get('subject')
                message = request.POST.get('message')
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get('email'), ]

                context = {
                    'name': name,
                    'subject': subject,
                    'message': message,
                }

                message = get_template("email.html").render(context)
                mail = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=email_from,
                    to=['riasadazim@gmail.com'],
                    reply_to=recipient_list,
                )
                mail.content_subtype = "html"
                mail.send()
                success = "Email sent successfully. We will get in touch with you soon."
                context = {'success': success, 'form': form}
            else:
                form = FormWithCaptcha()
                error = "Recaptcha validation failed."
                context = {'error': error, 'form': form}
                return render(request, 'contact.html', context)
        except Exception as e:
            error = f"Error: {e}"
            context = {'error': error, 'form': form}

        return render(request, 'contact.html', context)


# Sitemap
def sitemap(request):
    return render(request, 'sitemap.html', content_type="text/xml")