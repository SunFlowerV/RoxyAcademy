from RoxyAcademyApp.views import authViews, homeViews, pagesViews, coursesViews, dashboardViews, mainViews
from django.urls import path

urlpatterns = [
    path('', homeViews.singleCourse, name='home'),
    path('single-course', homeViews.singleCourse, name ='singleCourse'),

    # pages
    path('aboutus-01', pagesViews.aboutus01, name ='aboutus01'),
    path('aboutus-02', pagesViews.aboutus02, name ='aboutus02'),
    path('cart', pagesViews.cart, name ='cart'),
    path('contact', pagesViews.contact, name ='contact'),
    path('faqs', pagesViews.faqs, name ='faqs'),
    path('login', authViews.login_view, name='login'),
    path('register', authViews.register_view, name='register'),
    path('logout', authViews.logout_view, name='logout'),
    path('maintenance', pagesViews.maintenance, name ='maintenance'),
    path('my-account', pagesViews.myAccount, name ='myAccount'),
    path('page-error', pagesViews.pageError, name ='pageError'),
    path('privacy-policy', pagesViews.privacyPolicy, name ='privacyPolicy'),
    path('profile', pagesViews.profile, name ='profile'),
    path('shop', pagesViews.shop, name ='shop'),
    path('single-product', pagesViews.singleProduct, name ='singleProduct'),
    
    # courses
    path('course-details', coursesViews.courseDetails, name ='courseDetails'),
    path('course-details-2', coursesViews.courseDetails2, name ='courseDetails2'),
    path('course-details-3', coursesViews.courseDetails3, name ='courseDetails3'),
    path('create-course', coursesViews.createCourse, name ='createCourse'),
    path('edit-course/<int:course_id>', coursesViews.createCourse, name='editCourse'),
    path('instructor-course', coursesViews.instructorCourse, name ='instructorCourse'),
    path('lesson', coursesViews.lesson, name ='lesson'),

    # dashboard/Instructor-dashboard
    path('instructor-announcements', dashboardViews.instructorAnnouncements, name ='instructorAnnouncements'),
    path('instructor-assignments', dashboardViews.instructorAssignments, name ='instructorAssignments'),
    path('instructor-dashboard', dashboardViews.instructorDashboard, name ='instructorDashboard'),
    path('instructor-enrolled-courses', dashboardViews.instructorEnrolledCourses, name ='instructorEnrolledCourses'),
    path('instructor-my-quiz-attempts', dashboardViews.instructorMyQuizAttempts, name ='instructorMyQuizAttempts'),
    path('instructor-order-history', dashboardViews.instructorOrderHistory, name ='instructorOrderHistory'),
    path('instructor-profile', dashboardViews.instructorProfile, name ='instructorProfile'),
    path('instructor-quiz-attempts', dashboardViews.instructorQuizAttempts, name ='instructorQuizAttempts'),
    path('instructor-reviews', dashboardViews.instructorReviews, name ='instructorReviews'),
    path('instructor-settings', dashboardViews.instructorSettings, name ='instructorSettings'),
    
    # dashboard/Student-dashboard
    path('student-dashboard', dashboardViews.studentDashboard, name ='studentDashboard'),
    path('student-enrolled-courses', dashboardViews.studentEnrolledCourses, name ='studentEnrolledCourses'),
    path('student-my-quiz-attempts', dashboardViews.studentMyQuizAttempts, name ='studentMyQuizAttempts'),
    path('student-order-history', dashboardViews.studentOrderHistory, name ='studentOrderHistory'),
    path('student-profile', dashboardViews.studentProfile, name ='studentProfile'),
    path('student-reviews', dashboardViews.studentReviews, name ='studentReviews'),
    path('student-settings', dashboardViews.studentSettings, name ='studentSettings'),
    
    # main
    path('all-questions', mainViews.allQuestions, name ='allQuestions'),
    path('header-layout', mainViews.headerLayout, name ='headerLayout'),
    path('lesson-assignments', mainViews.lessonAssignments, name ='lessonAssignments'),
    path('lesson-assignments-submit', mainViews.lessonAssignmentsSubmit, name ='lessonAssignmentsSubmit'),
    path('lesson-intro', mainViews.lessonIntro, name ='lessonIntro'),
    path('lesson-quiz', mainViews.lessonQuiz, name ='lessonQuiz'),
    path('lesson-quiz-result', mainViews.lessonQuizResult, name ='lessonQuizResult'),
    path('modal', mainViews.modal, name ='modal'),
    path('pagination-quiz', mainViews.paginationQuiz, name ='paginationQuiz'),
    path('purchase-guide', mainViews.purchaseGuide, name ='purchaseGuide'),
    path('questions-types', mainViews.questionsTypes, name ='questionsTypes'),
    path('quiz-with-custom-timer', mainViews.quizWithCustomTimer, name ='quizWithCustomTimer'),
    path('quiz-with-point', mainViews.quizWithPoint, name ='quizWithPoint'),
    path('sample-page-one', mainViews.samplePageOne, name ='samplePageOne'),
    path('sample-page-two', mainViews.samplePageTwo, name ='samplePageTwo'),
    path('single-question', mainViews.singleQuestion, name ='singleQuestion'),

]
