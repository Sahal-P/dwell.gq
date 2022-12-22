
from django.urls import path
from . import views
from . import helpers

urlpatterns = [ 
     path("",views.home,name="home"),
     path("userlogin/",views.user_login,name="user_login"),
     path("user_signup",views.user_signup,name="user_signup"),
     path("log_out",views.log_out,name="log_out"),
     path("log_in",views.log_in,name="log_in"),
     path("signup_otp_v",views.signup_otp_v,name="signup_otp_v"),
     path("d_admin",views.d_admin,name="d_admin"),
     path("user_otp",views.user_otp,name="user_otp"),
     path("otp_v/",views.otp_v,name="otp_v"),
     path("resendotp",views.resendotp, name="resendotp"),
     path("adminlogin",views. adminlogin,name="adminlogin"),
     path("adminlogout",views. adminlogout,name="adminlogout"),
     path("sales_report" , views.sales_report , name="sales_report"),
     path("generatesalesReportPdf/",helpers.generatesalesReportPdf,name="generatesalesReportPdf"),
     path("GenerateInvoicePdf",helpers.GenerateInvoicePdf,name="GenerateInvoicePdf"),
     path("GenerateCSV",helpers.GenerateCSV,name="GenerateCSV"),
     path("banner", views.banner, name="banner"),
     path("add_banner", views.add_banner, name="add_banner"),
     path("home3", views.home3, name="home3"),
     path("BannerSelect", views.BannerSelect, name="BannerSelect"),
     path("Remove_banner", views.Remove_banner, name="Remove_banner"),
     path("searchproduct", views.searchproduct, name="searchproduct"),
  
]
