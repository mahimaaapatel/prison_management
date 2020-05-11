from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import pyrebase
config={
    
    'apiKey': "AIzaSyBRRbUKVoA5jbgEzkWJn_-0TYsIN7xpibo",
    'authDomain': "prison-54644.firebaseapp.com",
    'databaseURL': "https://prison-54644.firebaseio.com",
    'projectId': "prison-54644",
    'storageBucket': "prison-54644.appspot.com",
    'messagingSenderId': "697584156491",
   ' appId': "1:697584156491:web:a365e543b04d31ff89b2ce",
    'measurementId': "G-YG2Q5TV4N2"
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def signIn(request):
    return render(request,"signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw=request.POST.get("pass")
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid email or password"
        return render(request, "signIn.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request, "signIn.html")

def signUp(request):
    return render(request, "signUp.html")
def postsignUp(request):
    name=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user=authe.create_user_with_email_and_password(email,password)
    except:
        message=("Please enter correct details.")
        return render(request,"signUp.html",{"message":message})
    uid=user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")
def Prisoners(request):
    return render(request,"prisoners.html")

def addPrisoner(request):
    return render(request,"addprisoner.html")

def postaddprisoner(request):

    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    prisonerName=request.POST.get('name')
    prisonerID=request.POST.get('id')
    cellNo=request.POST.get('cellno')
    photo=request.POST.get('img1')
    fingerprint=request.POST.get('img2')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    crimedetails=request.POST.get('details')
    arrival=request.POST.get('arrival')
    duration=request.POST.get('duration')
    url1=request.POST.get('url1')
    url2=request.POST.get('url2')
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    data = {
        "prisonerName": prisonerName,
        "prisonerID": prisonerID,
        "cellNo": cellNo,
        "photo": photo,
        "fingerprint": fingerprint,
        "state": state,
        "pincode": pincode,
        "crimedetails": crimedetails,
        "arrival": arrival,
        "duration": duration,
        "photo": url1,
        "fingerprint":url2
        
    }
    database.child('users').child(a).child('info').child('prisoners').child(millis).set(data)

    return render(request,"prisoners.html")

def viewPrisoner(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').child('prisoners').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child(a).child('info').child('prisoners').child(i).child('prisonerName').get().val()
        name.append(nam)
    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis=zip(lis_time,date,name)


    return render(request,"viewprisoner.html",{'comb_lis':comb_lis})

def post_check(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('info').child('prisoners').child(time).child('prisonerName').get().val()
    print(name)
    id = database.child('users').child(a).child('info').child('prisoners').child(time).child('prisonerID').get().val()
    cellNo = database.child('users').child(a).child('info').child('prisoners').child(time).child('cellNo').get().val()
    photo = database.child('users').child(a).child('info').child('prisoners').child(time).child('photo').get().val()
    fingerprint = database.child('users').child(a).child('info').child('prisoners').child(time).child('fingerprint').get().val()
    state = database.child('users').child(a).child('info').child('prisoners').child(time).child('state').get().val()
    pincode = database.child('users').child(a).child('info').child('prisoners').child(time).child('pincode').get().val()
    crimedetails = database.child('users').child(a).child('info').child('prisoners').child(time).child('crimedetails').get().val()
    arrival = database.child('users').child(a).child('info').child('prisoners').child(time).child('arrival').get().val()
    duration = database.child('users').child(a).child('info').child('prisoners').child(time).child('duration').get().val()

    return render(request,'post_check.html',{'name':name,'id':id,'cellNo':cellNo,'photo':photo,'fingerprint':fingerprint,'state':state,'pincode':pincode,'crimedetails':crimedetails,'arrival':arrival,'duration':duration})

def Guards(request):
    return render(request,"guards.html")

def addGuard(request):
    return render(request,"addGuard.html")

def postaddguard(request):

    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    name=request.POST.get('name')
    guardID=request.POST.get('id')
    block=request.POST.get('block')
    photo=request.POST.get('img3')
    gender=request.POST.get('gender')
    address=request.POST.get('address')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    url3=request.POST.get('url3')
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    data = {
        "Name": name,
        "guardID": guardID,
        "block": block,
        "photo": photo,
        "gender": gender,
        "address": address,
        "state": state,
        "pincode": pincode,
        "photo": url3
        
    }
    database.child('users').child(a).child('info').child('guards').child(millis).set(data)
   

    return render(request,"guards.html", )

def viewGuards(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').child('guards').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child(a).child('info').child('guards').child(i).child('Name').get().val()
        print(nam)
        name.append(nam)
    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis=zip(lis_time,date,name)

    return render(request,"viewGuards.html",{'comb_lis':comb_lis})

def post_check2(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('info').child('guards').child(time).child('Name').get().val()
    print(name)
    id = database.child('users').child(a).child('info').child('guards').child(time).child('guardID').get().val()
    block = database.child('users').child(a).child('info').child('guards').child(time).child('block').get().val()
    photo = database.child('users').child(a).child('info').child('guards').child(time).child('photo').get().val()
    gender = database.child('users').child(a).child('info').child('guards').child(time).child('gender').get().val()
    address = database.child('users').child(a).child('info').child('guards').child(time).child('address').get().val()
    state = database.child('users').child(a).child('info').child('guards').child(time).child('state').get().val()
    pincode = database.child('users').child(a).child('info').child('guards').child(time).child('pincode').get().val()

    return render(request,'post_check2.html',{'name':name,'id':id,'block':block,'photo':photo,'gender':gender,'address':address,'state':state,'pincode':pincode})


def postaddvisitor(request):
    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    name=request.POST.get('vname')
    photo=request.POST.get('img4')
    gender=request.POST.get('gender')
    email=request.POST.get('email')
    prisonerID=request.POST.get('id')
    address=request.POST.get('address')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    url4=request.POST.get('url4')
    data = {
        "Name": name,
        "photo": photo,
        "gender": gender,
        "email": email,
        "prisonerID": prisonerID,
        "address": address,
        "state": state,
        "pincode": pincode,
        "photo": url4

    }
    database.child('users').child('visitors').child(millis).set(data)

    return render(request,"signIn.html", )


def viewVisitors(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child('visitors').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child('visitors').child(i).child('Name').get().val()
        name.append(nam)
    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis=zip(lis_time,date,name)

    
    return render(request,"viewVisitors.html",{'comb_lis':comb_lis})

def post_check3(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child('visitors').child(time).child('Name').get().val()
    photo = database.child('users').child('visitors').child(time).child('photo').get().val()
    id = database.child('users').child('visitors').child(time).child('prisonerID').get().val()
    gender = database.child('users').child('visitors').child(time).child('gender').get().val()
    email = database.child('users').child('visitors').child(time).child('email').get().val()
    print(email)
    address = database.child('users').child('visitors').child(time).child('address').get().val()
    state = database.child('users').child('visitors').child(time).child('state').get().val()
    pincode = database.child('users').child('visitors').child(time).child('pincode').get().val()

    return render(request,'post_check3.html',{'name':name,'photo':photo,'id':id,'gender':gender,'email':email,'address':address,'state':state,'pincode':pincode})

def post_accept(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    email = database.child('users').child('visitors').child(time).child('email').get().val()
    print(email)
    database.child('users').child('visitors').child(time).remove()
    send_mail("Your visit has been accepted.", "Your visit has been accepted. Your visit has been scheduled on 05.06.2020.\nVisiting timings is from 10 AM to 2 PM. \nFollow all rules of protocol",'mahimap7@gmail.com', [email])
    return render(request,"welcome.html")

def post_reject(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("hiii")
    email = database.child('users').child('visitors').child(time).child('email').get().val()
    print(email)
    database.child('users').child('visitors').child(time).remove()
    send_mail("Your visit has been rejected.", "Your visit has been rejected. Please try again later",'mahimap7@gmail.com', [email])
    return render(request,"welcome.html")
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"blog.html")

def blog_single(request):
    return render(request,"blog-single.html")

def contact(request):
    return render(request,"contact.html")

def postcontact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    if(name and email and subject and message):
        send_mail(subject, ("Name: " +name+  "\n") + message, 'mahimap7@gmail.com', [email])
        mess=('Message sent.')
        return render(request,"contact.html",{"mess":mess})
    else:
        message=("Please fill in all the fields.")
        return render(request,"contact.html",{"message":message})
    

def portfolio(request):
    return render(request,"portfolio.html")

def services(request):
    return render(request,"services.html")

def vendor_partner(request):
    return render(request,"vendor_partner.html")

def postvendor(request):
    company_name = request.POST.get('company_name')
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    company_address = request.POST.get('company_address')
    services_offered = request.POST.get('services_offered')
    notes = request.POST.get('notes')
    if(company_name and name and email and phone and company_address ):
        mail = EmailMessage(company_name, services_offered, settings.EMAIL_HOST_USER , [email])
        mail.content_subtype = "html"
        catalog = request.FILES['catalog']
        mail.attach(catalog.name, catalog.read(), catalog.content_type)
        mail.send()
        mess=('Message sent.')
        return render(request,"vendor_partner.html",{"mess":mess})
    else:
        message=("Please fill in all the fields.")
        return render(request,"vendor_partner.html",{"message":message})

def postdesign(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    present_address = request.POST.get('present_address')
    permanent_address = request.POST.get('permanent_address')
    resume = request.FILES['resume']
    portfolio = request.FILES['portfolio']
    notes = request.POST.get('notes')
    if(name and email and phone and present_address and resume and portfolio):
        mail = EmailMessage(name, phone, settings.EMAIL_HOST_USER , [email])
        mail.content_subtype = "html"
        mail.attach(resume.name, resume.read(), resume.content_type)
        mail.attach(portfolio.name, portfolio.read(), portfolio.content_type)
        mail.send()
        mess=('Message sent.')
        return render(request,"design_partner.html",{"mess":mess})
    else:
        message=("Please fill in all the fields.")
        return render(request,"design_partner.html",{"message":message})

def design_partner(request):
    return render(request,"design_partner.html")

def team(request):
    return render(request,"team.html")