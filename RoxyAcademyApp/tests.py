from io import BytesIO
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils.translation import override
from PIL import Image

from RoxyAcademyApp.models import Assignment, Course, Lesson, Quiz, Topic


class CourseContentModelTests(TestCase):
    def setUp(self):
        instructor = User.objects.create_user(
            username='content-model-instructor',
            password='correct-horse-battery-staple',
        )
        self.course = Course.objects.create(
            title='Course with structured content',
            description='Course description.',
            author=instructor,
        )

    def test_course_topics_contain_ordered_lessons_quizzes_and_assignments(self):
        topic = Topic.objects.create(
            course=self.course,
            title='Introduction',
            summary='The first topic.',
            order=1,
        )
        later_topic = Topic.objects.create(
            course=self.course,
            title='Advanced topics',
            order=2,
        )
        first_lesson = Lesson.objects.create(topic=topic, title='First lesson', order=1)
        second_lesson = Lesson.objects.create(topic=topic, title='Second lesson', order=2)
        quiz = Quiz.objects.create(topic=topic, title='Knowledge check')
        assignment = Assignment.objects.create(topic=topic, title='Practice task')

        self.assertEqual(list(self.course.topics.all()), [topic, later_topic])
        self.assertEqual(list(topic.lessons.all()), [first_lesson, second_lesson])
        self.assertEqual(list(topic.quizzes.all()), [quiz])
        self.assertEqual(list(topic.assignments.all()), [assignment])

class CourseCreationTests(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='course-instructor',
            email='course-instructor@example.com',
            password='correct-horse-battery-staple',
        )
        instructor_group, _ = Group.objects.get_or_create(name='Instructor')
        self.instructor.groups.add(instructor_group)
        self.client.force_login(self.instructor)

    def test_instructor_can_save_course_and_intro_video(self):
        thumbnail_buffer = BytesIO()
        Image.new('RGB', (1, 1)).save(thumbnail_buffer, format='PNG')
        response = self.client.post(
            reverse('createCourse'),
            {
                'title': 'Python Basics',
                'slug': '',
                'description': 'An introduction to Python.',
                'difficulty': Course.DIFFICULTY_BEGINNER,
                'price': '20',
                'thumbnail': SimpleUploadedFile(
                    'cover.png',
                    thumbnail_buffer.getvalue(),
                    content_type='image/png',
                ),
                'intro_video_file': SimpleUploadedFile(
                    'introduction.mp4',
                    b'video content',
                    content_type='video/mp4',
                ),
            },
        )

        course = Course.objects.get(title='Python Basics')
        self.assertRedirects(response, reverse('instructorCourse'))
        self.assertEqual(course.author, self.instructor)
        self.assertEqual(course.slug, 'python-basics')
        self.assertEqual(course.price, Decimal('20.00'))
        self.assertFalse(course.is_free)
        self.assertEqual(course.status, Course.STATUS_DRAFT)
        self.assertTrue(course.thumbnail.storage.exists(course.thumbnail.name))
        self.assertTrue(course.intro_video_file.storage.exists(course.intro_video_file.name))
    def test_free_course_is_saved_with_zero_price(self):
        response = self.client.post(
            reverse('createCourse'),
            {
                'title': 'Free Course',
                'description': 'Free course details.',
                'difficulty': Course.DIFFICULTY_BEGINNER,
                'is_free': 'on',
                'price': '',
            },
        )

        course = Course.objects.get(title='Free Course')
        self.assertRedirects(response, reverse('instructorCourse'))
        self.assertTrue(course.is_free)
        self.assertEqual(course.price, Decimal('0.00'))

    def test_paid_course_requires_a_positive_price(self):
        response = self.client.post(
            reverse('createCourse'),
            {
                'title': 'Course Without Price',
                'description': 'Course description.',
                'difficulty': Course.DIFFICULTY_BEGINNER,
                'price': '',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('price', response.context['form'].errors)
        self.assertFalse(Course.objects.filter(title='Course Without Price').exists())

    def test_paid_course_price_must_be_an_integer(self):
        response = self.client.post(
            reverse('createCourse'),
            {
                'title': 'Fractional Price Course',
                'description': 'Course with an invalid fractional price.',
                'difficulty': Course.DIFFICULTY_BEGINNER,
                'price': '19.99',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('price', response.context['form'].errors)
        self.assertFalse(Course.objects.filter(title='Fractional Price Course').exists())

    def test_all_levels_difficulty_is_available_and_saved(self):
        response = self.client.post(
            reverse('createCourse'),
            {
                'title': 'All Levels Course',
                'description': 'Course for learners at every level.',
                'difficulty': Course.DIFFICULTY_ALL_LEVELS,
                'is_free': 'on',
                'price': '',
            },
        )

        course = Course.objects.get(title='All Levels Course')
        self.assertRedirects(response, reverse('instructorCourse'))
        self.assertEqual(course.difficulty, Course.DIFFICULTY_ALL_LEVELS)

    def test_instructor_can_edit_own_course(self):
        thumbnail_buffer = BytesIO()
        Image.new('RGB', (1, 1)).save(thumbnail_buffer, format='PNG')
        course = Course.objects.create(
            title='Old course title',
            description='Old description.',
            author=self.instructor,
            status=Course.STATUS_PUBLISHED,
            thumbnail=SimpleUploadedFile(
                'existing-cover.png',
                thumbnail_buffer.getvalue(),
                content_type='image/png',
            ),
            intro_video_file=SimpleUploadedFile(
                'existing-intro.mp4',
                b'existing video content',
                content_type='video/mp4',
            ),
        )
        thumbnail_name = course.thumbnail.name
        video_name = course.intro_video_file.name

        edit_url = reverse('editCourse', args=[course.pk])
        get_response = self.client.get(edit_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTrue(get_response.context['is_edit'])
        self.assertEqual(get_response.context['form'].instance, course)
        self.assertContains(get_response, 'id="Lesson"')
        self.assertContains(get_response, 'data-bs-target="#Lesson"')
        self.assertContains(get_response, 'Обычная цена (₽)')
        self.assertContains(get_response, 'value="0"')
        self.assertContains(get_response, course.thumbnail.url)
        self.assertContains(get_response, course.intro_video_file.url)

        post_response = self.client.post(
            edit_url,
            {
                'title': 'Updated course title',
                'slug': '',
                'description': 'Updated description.',
                'difficulty': Course.DIFFICULTY_INTERMEDIATE,
                'price': '25',
            },
        )

        self.assertRedirects(post_response, reverse('instructorCourse'))
        course.refresh_from_db()
        self.assertEqual(course.title, 'Updated course title')
        self.assertEqual(course.description, 'Updated description.')
        self.assertEqual(course.difficulty, Course.DIFFICULTY_INTERMEDIATE)
        self.assertEqual(course.author, self.instructor)
        self.assertEqual(course.status, Course.STATUS_PUBLISHED)
        self.assertEqual(course.price, Decimal('25.00'))
        self.assertEqual(course.thumbnail.name, thumbnail_name)
        self.assertEqual(course.intro_video_file.name, video_name)

    def test_instructor_cannot_edit_another_instructors_course(self):
        other_instructor = User.objects.create_user(
            username='another-course-instructor',
            password='correct-horse-battery-staple',
        )
        course = Course.objects.create(
            title='Private course',
            description='Private course description.',
            author=other_instructor,
        )

        response = self.client.get(reverse('editCourse', args=[course.pk]))

        self.assertEqual(response.status_code, 404)

    def test_instructor_courses_page_lists_only_own_courses_by_status(self):
        published_course = Course.objects.create(
            title='Published Python',
            description='Published course description.',
            author=self.instructor,
            status=Course.STATUS_PUBLISHED,
            is_free=False,
            price=125,
        )
        archived_course = Course.objects.create(
            title='Archived Python',
            description='Archived course description.',
            author=self.instructor,
            status=Course.STATUS_ARCHIVED,
        )
        draft_course = Course.objects.create(
            title='Draft Python',
            description='Draft course description.',
            author=self.instructor,
            status=Course.STATUS_DRAFT,
        )
        other_instructor = User.objects.create_user(
            username='another-instructor',
            password='correct-horse-battery-staple',
        )
        Course.objects.create(
            title='Another Instructor Course',
            description='This course must not be listed.',
            author=other_instructor,
            status=Course.STATUS_PUBLISHED,
        )

        response = self.client.get(reverse('instructorCourse'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published_course.title)
        self.assertContains(response, '125 ₽')
        self.assertContains(response, archived_course.title)
        self.assertContains(response, draft_course.title)
        self.assertNotContains(response, 'Another Instructor Course')
        self.assertContains(response, reverse('editCourse', args=[published_course.pk]))
        self.assertQuerySetEqual(response.context['published_courses'], [published_course])
        self.assertQuerySetEqual(response.context['archived_courses'], [archived_course])
        self.assertQuerySetEqual(response.context['draft_courses'], [draft_course])

    def test_empty_course_statuses_have_russian_translations(self):
        with override('ru'):
            response = self.client.get(reverse('instructorCourse'))

        self.assertContains(response, 'Пока нет опубликованных курсов.')
        self.assertContains(response, 'В архиве пока нет курсов.')
        self.assertContains(response, 'Пока нет черновиков курсов.')
        self.assertContains(response, 'Архив')

    def test_difficulty_levels_have_russian_translations_on_courses_page(self):
        levels = (
            Course.DIFFICULTY_ALL_LEVELS,
            Course.DIFFICULTY_BEGINNER,
            Course.DIFFICULTY_INTERMEDIATE,
            Course.DIFFICULTY_ADVANCED,
            Course.DIFFICULTY_EXPERT,
        )
        for index, level in enumerate(levels):
            Course.objects.create(
                title=f'Course level {index}',
                description='Course description.',
                author=self.instructor,
                status=Course.STATUS_PUBLISHED,
                difficulty=level,
            )

        with override('ru'):
            response = self.client.get(reverse('instructorCourse'))

        for translated_level in ('Все уровни', 'Начинающий', 'Средний уровень', 'Продвинутый', 'Эксперт'):
            self.assertContains(response, translated_level)

class InstructorRoleTests(TestCase):
    def test_admin_assigned_instructor_gets_dashboard_access_without_admin_access(self):
        instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='correct-horse-battery-staple',
        )
        instructor_group, _ = Group.objects.get_or_create(name='Instructor')
        instructor.groups.add(instructor_group)
        self.client.force_login(instructor)

        self.assertEqual(self.client.get(reverse('instructorDashboard')).status_code, 200)
        self.assertEqual(self.client.get(reverse('instructorAssignments')).status_code, 200)
        courses_response = self.client.get(reverse('instructorCourse'))
        self.assertEqual(courses_response.status_code, 200)
        self.assertTemplateUsed(
            courses_response,
            'dashboard/InstructorDashboard/instructorCourses.html',
        )
        self.assertContains(courses_response, f'href="{reverse("instructorCourse")}"')
        self.assertContains(courses_response, 'id="archived-tab-4"')
        self.assertNotContains(courses_response, "pending-tab-4")
        self.assertEqual(self.client.get(reverse('createCourse')).status_code, 200)
        admin_response = self.client.get('/admin/')
        self.assertEqual(admin_response.status_code, 302)
        self.assertTrue(admin_response.url.startswith(reverse('admin:login')))

    def test_public_registration_cannot_create_instructor(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'instructor',
                'email': 'instructor@example.com',
                'password1': 'correct-horse-battery-staple',
                'password2': 'correct-horse-battery-staple',
                'role': 'instructor',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='instructor').exists())
        self.assertFalse(Group.objects.filter(name='Instructor').exists())

    def test_student_cannot_access_instructor_dashboard(self):
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password',
        )
        self.client.force_login(student)

        response = self.client.get(reverse('instructorDashboard'))
        create_course_response = self.client.get(reverse('createCourse'))
        instructor_courses_response = self.client.get(reverse('instructorCourse'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        self.assertEqual(create_course_response.status_code, 302)
        self.assertEqual(instructor_courses_response.status_code, 302)

    def test_public_registration_cannot_create_admin(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'attacker',
                'email': 'attacker@example.com',
                'password1': 'correct-horse-battery-staple',
                'password2': 'correct-horse-battery-staple',
                'role': 'admin',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='attacker').exists())
        self.assertFalse(Group.objects.filter(name='Instructor').exists())


class SingleCourseHomeTests(TestCase):
    def test_single_course_is_available_at_root_and_removed_home_urls_return_404(self):
        home_response = self.client.get('/')
        single_course_response = self.client.get(reverse('singleCourse'))

        self.assertEqual(home_response.status_code, 200)
        self.assertTemplateUsed(home_response, 'home/singleCourse.html')
        self.assertEqual(single_course_response.status_code, 200)
        self.assertEqual(self.client.get('/marketplace').status_code, 404)
        self.assertEqual(self.client.get('/main-demo').status_code, 404)
        self.assertEqual(self.client.get('/art-design-school').status_code, 404)


    def test_wishlist2_page_is_removed(self):
        self.assertEqual(self.client.get('/wishlist-2').status_code, 404)

    def test_requested_pages_are_removed(self):
        removed_urls = (
            '/academy-gallery',
            '/admission-guide',
            '/become-teacher',
            '/event-grid',
            '/event-details',
            '/event-list',
            '/event-sidebar',
            '/instructor',
            '/subscription',
            '/instructor-wishlist',
            '/student-wishlist',
        )
        for url in removed_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_home_and_courses_menus_are_removed_and_logos_link_home(self):
        response = self.client.get('/')
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertRegex(content, r'<a href="/">\s*<img src="/static/images/logo/roxy-academy\.svg"')
        self.assertRegex(content, r'<a href="/">\s*<img src="/static/images/dark/logo/roxy-academy-light\.svg"')
        self.assertNotRegex(content, r'Home\s*<i class="feather-chevron-down"')
        self.assertNotRegex(content, r'Courses\s*<i class="feather-chevron-down"')

    def test_dashboard_and_pages_menus_are_removed_from_headers(self):
        for url in ('/', reverse('courseDetails')):
            with self.subTest(url=url):
                response = self.client.get(url)
                content = response.content.decode()

                self.assertEqual(response.status_code, 200)
                self.assertNotRegex(content, r'<a href="#">Dashboard\s*<i class="feather-chevron-down"')
                self.assertNotRegex(content, r'<a href="#">Pages\s*<i class="feather-chevron-down"')

    def test_search_control_is_removed_from_site_headers(self):
        for url in ('/', reverse('courseDetails')):
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, 'search-trigger-active')
                self.assertNotContains(response, 'rbt-search-dropdown')
                self.assertNotContains(response, 'rbt-cart-sidenav-activation')

    def test_home_instructor_block_uses_shared_theme_gradient(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'class="rbt-author-area bg-gradient-8 home-instructor-area rbt-section-gap"',
        )

    def test_category_menu_is_removed_from_page_header(self):
        response = self.client.get(reverse('courseDetails'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'rbt-category-menu-wrapper')

    def test_blog_pages_and_menu_are_removed(self):
        response = self.client.get('/')
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(content, r'<a href="#">Blog\s*<i class="feather-chevron-down"')

        removed_blog_urls = (
            '/blog',
            '/blog-details',
            '/blog-grid-minimal',
            '/blog-list',
            '/blog-with-sidebar',
            '/post-format-audio',
            '/post-format-gallery',
            '/post-format-quote',
            '/post-format-standard',
            '/post-format-video',
        )
        for url in removed_blog_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_element_pages_and_menu_are_removed(self):
        response = self.client.get('/')
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(content, r'<a href="#">Elements\s*<i class="feather-chevron-down"')

        removed_element_urls = (
            '/about',
            '/accordion',
            '/advancetab',
            '/badge',
            '/brand',
            '/button',
            '/call-to-action',
            '/card',
            '/category',
            '/counterup',
            '/elements',
            '/gallery',
            '/header',
            '/instagram',
            '/listStyle',
            '/newsletter',
            '/pricing',
            '/progressbar',
            '/search',
            '/service',
            '/social',
            '/split',
            '/style-guide',
            '/team',
            '/testimonial',
        )
        for url in removed_element_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_lesson_page_renders_without_url_reverse_errors(self):
        response = self.client.get(reverse('lesson'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/lesson.html')
        self.assertNotContains(response, 'rbt-header-wrapper')
        self.assertNotContains(response, 'rbt-progress-parent')
        self.assertNotContains(response, 'rbt-footer')

    def test_lesson_intro_page_renders_and_uses_registered_route(self):
        response = self.client.get(reverse('lessonIntro'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessonIntro.html')
        self.assertContains(response, 'href="/lesson-intro"')

    def test_course_catalog_pages_are_removed_but_course_detail_remains(self):
        removed_catalog_urls = (
            '/course-card-2',
            '/course-card-3',
            '/course-filter-one-open',
            '/course-filter-one-toggle',
            '/course-filter-two-open',
            '/course-filter-two-toggle',
            '/course-masonry',
            '/course-with-sidebar',
            '/course-with-tab',
            '/course-with-tab-two',
        )
        for url in removed_catalog_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

        course_detail_response = self.client.get(reverse('courseDetails'))
        self.assertEqual(course_detail_response.status_code, 200)
        self.assertTemplateUsed(course_detail_response, 'courses/courseDetails.html')


class LanguageSelectionTests(SimpleTestCase):
    def test_russian_is_default_and_english_has_a_language_prefix(self):
        russian_response = self.client.get('/')
        english_response = self.client.get('/en/')

        self.assertEqual(russian_response.status_code, 200)
        self.assertEqual(russian_response.context['LANGUAGE_CODE'], 'ru')
        self.assertContains(russian_response, '<html lang="ru">')
        self.assertContains(russian_response, 'name="language" value="en"')
        self.assertEqual(english_response.status_code, 200)
        self.assertEqual(english_response.context['LANGUAGE_CODE'], 'en')
        self.assertContains(english_response, '<html lang="en">')
        self.assertContains(english_response, 'name="language" value="ru"')

    def test_language_switch_preserves_the_current_page(self):
        response = self.client.post(
            reverse('set_language'),
            {'language': 'ru', 'next': '/course-details'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/course-details')
        self.assertEqual(response.cookies['django_language'].value, 'ru')

        russian_response = self.client.get(response.url)
        self.assertEqual(russian_response.context['LANGUAGE_CODE'], 'ru')

    def test_switching_to_english_adds_the_language_prefix(self):
        response = self.client.post(
            reverse('set_language'),
            {'language': 'en', 'next': '/en/course-details'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/en/course-details')
        self.assertEqual(response.cookies['django_language'].value, 'en')

    def test_language_switcher_posts_to_the_current_page_in_each_language(self):
        english_response = self.client.get('/en/course-details')
        russian_response = self.client.get('/course-details')

        self.assertContains(
            english_response,
            'name="next" value="/course-details"',
        )
        self.assertContains(
            english_response,
            'name="next" value="/en/course-details"',
        )
        self.assertContains(
            russian_response,
            'name="next" value="/course-details"',
        )
        self.assertContains(
            russian_response,
            'name="next" value="/en/course-details"',
        )

    def test_switching_from_an_english_page_returns_to_its_russian_version(self):
        english_response = self.client.get('/en/course-details')
        self.assertContains(
            english_response,
            'name="next" value="/course-details"',
        )

        switch_response = self.client.post(
            reverse('set_language'),
            {'language': 'ru', 'next': '/course-details'},
        )
        russian_response = self.client.get(switch_response.url)

        self.assertEqual(switch_response.status_code, 302)
        self.assertEqual(switch_response.url, '/course-details')
        self.assertEqual(russian_response.context['LANGUAGE_CODE'], 'ru')


class StudentDashboardButtonTests(TestCase):
    def test_student_dashboard_pages_do_not_show_become_instructor_button(self):
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password',
        )
        self.client.force_login(student)

        dashboard_pages = (
            'studentDashboard',
            'studentEnrolledCourses',
            'studentMyQuizAttempts',
            'studentOrderHistory',
            'studentProfile',
            'studentReviews',
            'studentSettings',
        )
        for page_name in dashboard_pages:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, 'Become an Instructor')
