from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
import uuid

# Assuming existing models like Department, Program, etc.

# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the Django User model for authentication
#     full_name = models.CharField(max_length=200)  # Full name of the teacher
#     # ... any other relevant fields ...

#     def __str__(self):
#         return self.full_name

# ... rest of your existing models ...


class Department(models.Model):
    dept_name = models.CharField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return str(self.dept_name)

    class Meta:
        db_table = 'department'


class Program(models.Model):
    program_name = models.CharField(max_length=100, blank=True, unique=True)
    department = models.ForeignKey(Department, on_delete=CASCADE)

    def __str__(self):
        return str(self.program_name)

    class Meta:
        db_table = 'program'


class StudentLoginInfo(models.Model):
    username = models.CharField(max_length=120, null=True, blank=False)
    roll_number = models.CharField(primary_key=True, max_length=9)
    department = models.ForeignKey(Department, on_delete=CASCADE)
    program = models.ForeignKey(Program, on_delete=CASCADE)
    password = models.CharField(max_length=100, null=True, blank=False)
    dob = models.DateField()
    gender = models.CharField(
        max_length=10, default="null", null=True, blank=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = 'StudentLoginInfo'


class Subject(models.Model):
    sub_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.sub_name)

    class Meta:
        db_table = 'subject'


class TeacherInfo(models.Model):
    unique_id = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=CASCADE)
    images = models.ImageField(
        upload_to='images/', blank=True, default="cute_baby.gif")
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'TeacherInfo'


class Template(models.Model):
    content = """
        <p>
          <br />I would like to {{quality.recommend}} recommend
          Mr.<b>{{student.name}}</b> for admission to the graduate program at your
          university. I have known {{firstname}} for about
          {{student.years_taught}} now as an undergraduate student in
          {{student.std.program}} Engineering. {%if student.is_pro == 'Yes'%}
          Moreover, I was the supervisor for his final year project. {%endif%}
          {% if value %} I taught him {{subject}}. {%else%} I taught him 
          {%for item in subjects %} {{item}}, {%endfor%} and {{subject}}. {%endif%}
        </p>

        <!-- Section Two -->
        <p>
          <br />I recall {{firstname}} as a {{quality.quality}} student. 
          {% if academics.tentative_ranking == "Batch Topper" %} In fact, he was the
          topper of his batch in {{student.std.program}} Engineering. {% else %}
          He maintained excellent academic performance throughout his
          undergraduate ranking among the {{academics.tentative_ranking}}
          students of his batch. {% endif %} As an instructor and his supervisor
          too I had enough opportunity is observe his capabilities closely.
        </p>

        <!-- Section Three -->
        <p>
          <br />

          {%if student.is_pro == 'Yes'%} I was the supervisor in his project
          titled {{project.supervised_project}}. I was quite impressed by his
          hardworking nature and learning capability. {%endif%} 
          {%if project.final_project%} I supervised him in his project
          {{project.final_project}}. I could observe his keen interest and
          aptitude for research while working on the project. {%endif%} 
          {%if student.is_paper == 'Yes'%} In fact, he was also able to publish a
          paper on {{paper.paper_title}}. {%endif%}
        </p>

        <!-- Section Four -->
        <p>
          <br />I have noted his {{quality.presentation}} presentation skills
          while he presented his work at our department as well as in the
          conference. {%if quality.leadership or quality.teamwork%} I have seen
          that he has good leadership capability and has a teamwork spirit.
          {%endif%} {%if quality.hardworking%} He is a very hardworking student
          who is always eager to learn. {%endif%} {%if quality.friendly%} He is
          a well-spoken person with a friendly and gentle personality. {%endif%}
          {%if quality.social%} He also has given his time to different social
          causes. {%endif%} He is very helpful and cooperative student. He
          eagerly handed over his project work to his juniors who wanted to
          further continue the research on the topic along with proper guidance
          and resources. I have also been impressed by his communication skills
          during project presentations and lectures.
        </p>

        <!-- Section Five -->
        <p>
          <br />I appreciate his technical and professional skills. 
          {%if quality.extracurricular != 'No'%} Besides academics, he was also
          involved in several extra-curricular activities . He participated in
          various competitions organized in and off the campus. {%endif%} 
          {%if project.deployed%} Unlike, most students who limit their project to an
          academic exercise, he actually deployed his project publicly in our
          server and maintained it. {%endif%} {%if student.intern%} He has
          worked in some IT companies which, I believe, has further added to his
          technical skills and professional experience. {%endif%}
        </p>

        <!-- Section Six -->
        <p>
          <br />I am quite confident that {{firstname}}'s skills coupled with
          academic capability will make him a good candidate for your
          university. Thus, I would highly recommend him for the graduate
          program at your esteemed university. Please feel free to contact me if
          further enquiry is required.
        </p>

        <p>
          <br />{{student.professor.name}}, <br />{{student.professor.title}},
          <br />Department of {{student.professor.department}} Engineering
          <br />Pulchowk Campus, Institute of Engineering, Tribhuvan University
          <br />Phone: {{student.professor.phone}} <br />Mail:
          {{student.professor.email}}
        </p>
        """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.OneToOneField(TeacherInfo, on_delete=models.CASCADE)
    content = models.TextField(default=content)

    def __str__(self):
        return f"Template for {self.teacher.name}"


class StudentData(models.Model):
    name = models.CharField(max_length=122, null=True, blank=True)
    universities = models.CharField(null=True, blank=True, max_length=1000)
    professor = models.ForeignKey(TeacherInfo, on_delete=CASCADE)
    std = models.ForeignKey(StudentLoginInfo, on_delete=CASCADE)
    is_generated = models.BooleanField(default=False)
    reapplied = models.BooleanField(default=False)
    years_taught = models.CharField(max_length=10, null=True, blank=True)
    is_pro = models.CharField(max_length=3, default="null")
    subjects = models.CharField(max_length=500, null=True, blank=True)
    is_paper = models.CharField(max_length=500, null=True, blank=True)
    intern = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'StudentData'


class Paper(models.Model):
    paper_title = models.CharField(max_length=100, null=True, blank=True)
    paper_link = models.CharField(max_length=200, null=True, blank=True)
    student = models.ForeignKey(StudentData, on_delete=CASCADE)

    def __str__(self):
        return str(self.paper_title)

    class Meta:
        db_table = 'Paper'


class Project(models.Model):
    supervised_project = models.CharField(
        max_length=100, null=True, blank=True)
    final_project = models.CharField(max_length=200, null=True, blank=True)
    deployed = models.BooleanField(default=False)
    student = models.ForeignKey(StudentData, on_delete=CASCADE)

    def __str__(self):
        return str(self.student) + str(self.supervised_project)

    class Meta:
        db_table = 'Project'


class University(models.Model):
    uni_name = models.CharField(max_length=100, null=True, blank=True)
    uni_deadline = models.DateField(null=True, blank=True)
    program_applied = models.CharField(max_length=100, null=True, blank=True)
    student = models.ForeignKey(StudentData, on_delete=CASCADE)

    def __str__(self):
        return str(self.student) + str(self.uni_name)

    class Meta:
        db_table = 'University'


class Qualities(models.Model):
    student = models.ForeignKey(StudentData, on_delete=CASCADE)

    leadership = models.BooleanField(default=False)
    hardworking = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    teamwork = models.BooleanField(default=False)
    friendly = models.BooleanField(default=False)

    quality = models.CharField(max_length=50, null=True, blank=True)
    presentation = models.CharField(max_length=50, null=True, blank=True)
    extracirricular = models.CharField(max_length=50, null=True, blank=True)

    recommend = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.student) + " Qualities"

    class Meta:
        db_table = 'Qualities'


class Academics(models.Model):
    student = models.ForeignKey(StudentData, on_delete=CASCADE)
    gpa = models.CharField(max_length=50, null=True, blank=True)
    tentative_ranking = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.student) + " Academics"

    class Meta:
        db_table = 'Academics'


class Files(models.Model):
    transcript = models.ImageField(upload_to='transcript/', blank=True)
    CV = models.ImageField(upload_to='cv/', blank=True)
    Photo = models.ImageField(upload_to='student_photo/', blank=True)
    student = models.ForeignKey(StudentData, on_delete=CASCADE)

    def __str__s(self):
        return str(self.student) + " Files"

    class Meta:
        db_table = 'Files'


# Assuming you're using Django's built-in User model for authentication
