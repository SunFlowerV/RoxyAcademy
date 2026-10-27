from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Course(models.Model):
    DIFFICULTY_ALL_LEVELS = 'all_levels'
    DIFFICULTY_BEGINNER = 'beginner'
    DIFFICULTY_INTERMEDIATE = 'intermediate'
    DIFFICULTY_ADVANCED = 'advanced'
    DIFFICULTY_EXPERT = 'expert'

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_ALL_LEVELS, 'All Levels'),
        (DIFFICULTY_BEGINNER, 'Beginner'),
        (DIFFICULTY_INTERMEDIATE, 'Intermediate'),
        (DIFFICULTY_ADVANCED, 'Advanced'),
        (DIFFICULTY_EXPERT, 'Expert'),
    ]

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField()
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_BEGINNER,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    thumbnail = models.ImageField(
        upload_to='courses/thumbnails/',
        blank=True,
        null=True,
    )
    intro_video_url = models.URLField(max_length=500, blank=True, null=True)
    intro_video_file = models.FileField(
        upload_to='courses/intro_videos/',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_courses',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'course'
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class CourseContentItem(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Topic(CourseContentItem):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='topics',
    )

    class Meta(CourseContentItem.Meta):
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class Lesson(CourseContentItem):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='lessons',
    )

    class Meta(CourseContentItem.Meta):
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


class Quiz(CourseContentItem):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='quizzes',
    )

    class Meta(CourseContentItem.Meta):
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'


class Assignment(CourseContentItem):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='assignments',
    )

    class Meta(CourseContentItem.Meta):
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
