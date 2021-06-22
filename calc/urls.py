
from django.urls import path
from .import views

# urlpatterns = [path("", views.index, name="index"),]
# app_name = "main"   
urlpatterns = [
    path("", views.index, name="index"),
    path("homepage", views.homepage, name="homepage"),
    path("homepage_admin", views.homepage_admin, name="homepage_admin"),
    path("complain_register", views.complain_register, name="complain_register"),
    path("about_us", views.about_us, name="about_us"),
    path("track", views.track, name="track"),
    path("tracknext", views.tracknext, name="tracknext"),
    path("verification_start", views.verification_start, name="verification_start"),
    path("verification_after_mail/<name>", views.verification_after_mail, name="verification_after_mail"),
    path("notes", views.notes, name="notes"),
    path("nxt_notes", views.nxt_notes, name="nxt_notes"),
    path("notes_verify", views.notes_verify, name="notes_verify"),
    path("notes_register", views.notes_register, name="notes_register"),
    path("notes_register_here", views.notes_register_here, name="notes_register_here"),
    path("verify_notes_by_teacher", views.verify_notes_by_teacher, name="verify_notes_by_teacher"),
    path("loginCC", views.loginCC, name="loginCC"),
    path("logout_request", views.logout_request, name="logout_request"),
    path("loginc_verify", views.loginc_verify, name="loginc_verify"),
    path('get-topics-ajax', views.get_topics_ajax, name="get_topics_ajax"),
    path('admin_add_subject', views.admin_add_subject, name="admin_add_subject"),
    path('admin', views.admin, name="admin"),
    path('delete_subject', views.delete_subject, name="delete_subject"),
    path('store_data_full', views.store_data_full, name="store_data_full"),
    path('delete_subject_query', views.delete_subject_query, name="delete_subject_query"),
    path('update_subject_query', views.update_subject_query, name="update_subject_query"),
    path('store_data', views.store_data, name="store_data"),
    path('show_subject_in_addsubject', views.show_subject_in_addsubject, name="show_subject_in_addsubject"),
    path('show_subject_in_addsubject2', views.show_subject_in_addsubject2, name="show_subject_in_addsubject2"),
    path('show_subject_in_addsubject3', views.show_subject_in_addsubject3, name="show_subject_in_addsubject3"),
    path('show_subject_in_addsubject4', views.show_subject_in_addsubject4, name="show_subject_in_addsubject4"),
    path('show_subject_in_addsubject5', views.show_subject_in_addsubject5, name="show_subject_in_addsubject5"),
    path('show_subject_in_addsubject6', views.show_subject_in_addsubject6, name="show_subject_in_addsubject6"),
    path('show_subject_in_addsubject6', views.show_subject_in_addsubject6, name="show_subject_in_addsubject6"),
    path('id_add_session_function', views.id_add_session_function, name="id_add_session_function"),
    path('id_add_after_session_function_for_semestervalue', views.id_add_after_session_function_for_semestervalue, name="id_add_after_session_function_for_semestervalue"),
    path('id_add', views.id_add, name="id_add"),
    path('id_delete', views.id_delete, name="id_delete"),
    path('delete_id_aftereveyrhting', views.delete_id_aftereveyrhting, name="delete_id_aftereveyrhting"),
    path('id_update', views.id_update, name="id_update"),
    path('update_id', views.update_id, name="update_id"),
    path("login_admin", views.login_admin, name="login_admin"),
    path("loginAdmin_verify", views.loginAdmin_verify, name="loginAdmin_verify"),
    path("logout_request_admin", views.logout_request_admin, name="logout_request_admin"),
    path("id_add_after_session_function_for_namevalue", views.id_add_after_session_function_for_namevalue, name="id_add_after_session_function_for_namevalue"),
    path("shownotes_to_admin", views.shownotes_to_admin, name="shownotes_to_admin"),
    path("shownotes_to_admin_after_session", views.shownotes_to_admin_after_session, name="shownotes_to_admin_after_session"),
   
    path('viewnotes_in_admin', views.viewnotes_in_admin, name="viewnotes_in_admin"),
    path('delet_notesinadmin', views.delet_notesinadmin, name="delet_notesinadmin"),
    
    ]

