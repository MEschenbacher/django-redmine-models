# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings

redmine_models_managed = getattr(settings, 'REDMINE_MODELS_MANAGED', False)


class Attachment(models.Model):
    container_id = models.IntegerField(blank=True, null=True)
    container_type = models.CharField(max_length=30, blank=True, null=True)
    filename = models.CharField(max_length=1024)
    disk_filename = models.CharField(max_length=1024)
    filesize = models.BigIntegerField()
    content_type = models.CharField(max_length=1024, blank=True, null=True)
    digest = models.CharField(max_length=64)
    downloads = models.IntegerField()
    author = models.ForeignKey("User", on_delete=models.RESTRICT)
    created_on = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    disk_directory = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "attachments"


class AuthSource(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    host = models.CharField(max_length=60, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    account = models.CharField(max_length=1024, blank=True, null=True)
    account_password = models.CharField(max_length=1024, blank=True, null=True)
    base_dn = models.CharField(max_length=255, blank=True, null=True)
    attr_login = models.CharField(max_length=30, blank=True, null=True)
    attr_firstname = models.CharField(max_length=30, blank=True, null=True)
    attr_lastname = models.CharField(max_length=30, blank=True, null=True)
    attr_mail = models.CharField(max_length=30, blank=True, null=True)
    onthefly_register = models.BooleanField()
    tls = models.BooleanField()
    filter = models.TextField(blank=True, null=True)
    timeout = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "auth_sources"


class Board(models.Model):
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    topics_count = models.IntegerField()
    messages_count = models.IntegerField()
    last_message = models.ForeignKey(
        "Message",
        related_name="board_where_last",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    parent = models.ForeignKey("Board", blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "boards"


class Change(models.Model):
    changeset = models.ForeignKey("Changeset", on_delete=models.RESTRICT)
    action = models.CharField(max_length=1)
    path = models.TextField()
    from_path = models.TextField(blank=True, null=True)
    from_revision = models.CharField(max_length=1024, blank=True, null=True)
    revision = models.CharField(max_length=1024, blank=True, null=True)
    branch = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "changes"


class ChangesetParent(models.Model):
    changeset = models.ForeignKey("Changeset", on_delete=models.RESTRICT)
    parent = models.IntegerField("Changeset")

    class Meta:
        managed = redmine_models_managed
        db_table = "changeset_parents"


class Changeset(models.Model):
    repository = models.ForeignKey("Repository", on_delete=models.RESTRICT)
    revision = models.CharField(max_length=255)
    committer = models.CharField(max_length=1024, blank=True, null=True)
    committed_on = models.DateTimeField()
    comments = models.TextField(blank=True, null=True)
    commit_date = models.DateField(blank=True, null=True)
    scmid = models.CharField(max_length=1024, blank=True, null=True)
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "changesets"
        unique_together = (("repository", "revision"),)


class ChangesetsIssue(models.Model):
    changeset = models.ForeignKey(Changeset, on_delete=models.RESTRICT)
    issue = models.ForeignKey("Issue", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "changesets_issues"
        unique_together = (("changeset", "issue"),)


class Checklist(models.Model):
    is_done = models.BooleanField(default=False)
    subject = models.CharField(max_length=255, blank=True, null=True, default=None)
    position = models.IntegerField(default=1)
    issue = models.ForeignKey("Issue", on_delete=models.RESTRICT)
    created_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)
    is_section = models.BooleanField(default=False)

    class Meta:
        managed = redmine_models_managed
        db_table = "checklists"


class Comment(models.Model):
    commented_type = models.CharField(max_length=30)
    commented_id = models.IntegerField()
    author = models.ForeignKey("User", on_delete=models.RESTRICT)
    content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    class Meta:
        managed = redmine_models_managed
        db_table = "comments"


class CustomFieldEnumeration(models.Model):
    custom_field = models.ForeignKey("CustomField", on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024)
    active = models.BooleanField()
    position = models.IntegerField()

    class Meta:
        managed = redmine_models_managed
        db_table = "custom_field_enumerations"


class CustomField(models.Model):
    type = models.CharField(
        max_length=30,
        choices=(
            ("IssueCustomField", "Issue Custom Field"),
            ("TimeEntryCustomField", "Time Entry Custom Field"),
            ("ProjectCustomField", "Project Custom Field"),
            ("VersionCustomField", "Version Custom Field"),
            ("DocumentCustomField", "Document Custom Field"),
            ("UserCustomField", "User Custom Field"),
            ("GroupCustomField", "Group Custom Field"),
            (
                "TimeEntryActivityCustomField",
                "Time Entry Activity Custom Field"
            ),
            ("IssuePriorityCustomField", "Issue Priority Custom Field"),
            ("DocumentCategoryCustomField", "Document Category Custom Field"),
        ),
    )
    name = models.CharField(max_length=30)
    field_format = models.CharField(
        max_length=30,
        choices=(
            ("bool", "Boolean"),
            ("date", "Date"),
            ("int", "Integer"),
            ("link", "Link"),
            ("list", "List"),
            ("enumeration", "Key/value list"),
            ("float", "Float"),
            ("string", "Text"),
            ("text", "Long text"),
            ("user", "User"),
            ("version", "Version"),
        ),
    )
    possible_values = models.TextField(blank=True, null=True)
    regexp = models.CharField(max_length=1024, blank=True, null=True)
    min_length = models.IntegerField(blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    is_required = models.BooleanField()
    is_for_all = models.BooleanField()
    is_filter = models.BooleanField()
    position = models.IntegerField(blank=True, null=True)
    searchable = models.BooleanField(null=True, blank=True)
    default_value = models.TextField(blank=True, null=True)
    editable = models.BooleanField(null=True, blank=True)
    visible = models.BooleanField()
    multiple = models.BooleanField(null=True, blank=True)
    format_store = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "custom_fields"


class CustomFieldProject(models.Model):
    custom_field = models.ForeignKey(CustomField, on_delete=models.RESTRICT)
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "custom_fields_projects"
        unique_together = (("custom_field", "project"),)


class CustomFieldRole(models.Model):
    custom_field = models.ForeignKey(CustomField, on_delete=models.RESTRICT)
    role = models.ForeignKey("Role", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "custom_fields_roles"
        unique_together = (("custom_field", "role"),)


class CustomFieldTracker(models.Model):
    custom_field = models.ForeignKey(CustomField, on_delete=models.RESTRICT)
    tracker = models.ForeignKey("Tracker", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "custom_fields_trackers"
        unique_together = (("custom_field", "tracker"),)


class CustomValue(models.Model):
    customized_type = models.CharField(max_length=30)
    customized_id = models.IntegerField()
    custom_field = models.ForeignKey(CustomField, on_delete=models.RESTRICT)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "custom_values"


class Document(models.Model):
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)
    category = models.ForeignKey("IssueCategory", on_delete=models.RESTRICT)
    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "documents"


class EmailAddress(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    address = models.CharField(max_length=1024, unique=True)
    is_default = models.BooleanField()
    notify = models.BooleanField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    class Meta:
        managed = redmine_models_managed
        db_table = "email_addresses"


class EnabledModule(models.Model):
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024)

    class Meta:
        managed = redmine_models_managed
        db_table = "enabled_modules"


class Enumeration(models.Model):
    name = models.CharField(max_length=30)
    position = models.IntegerField(blank=True, null=True)
    is_default = models.BooleanField()
    type = models.CharField(
        blank=True,
        null=True,
        max_length=17,
        choices=(
            ("DocumentCategory", "Document Category"),
            ("IssuePriority", "Issue Priority"),
            ("TimeEntryActivity", "Time Entry Activity"),
        )
    )
    active = models.BooleanField()
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.RESTRICT)
    parent = models.ForeignKey("Enumeration", blank=True, null=True, on_delete=models.RESTRICT)
    position_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "enumerations"


class GroupUser(models.Model):
    group = models.ForeignKey("User", related_name="users", on_delete=models.RESTRICT)
    user = models.ForeignKey("User", related_name="groups", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "groups_users"
        unique_together = (("group", "user"),)


class ImportItem(models.Model):
    import_id = models.ForeignKey("Import", on_delete=models.RESTRICT)
    position = models.IntegerField()
    obj_id = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "import_items"


class Import(models.Model):
    type = models.CharField(max_length=1024, blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    filename = models.CharField(max_length=1024, blank=True, null=True)
    settings = models.TextField(blank=True, null=True)
    total_items = models.IntegerField(blank=True, null=True)
    finished = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = redmine_models_managed
        db_table = "imports"


class IssueCategory(models.Model):
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)
    name = models.CharField(max_length=60)
    assigned_to = models.ForeignKey("User", blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "issue_categories"


class IssueRelation(models.Model):
    issue_from = models.ForeignKey("Issue", related_name="related_to",
            on_delete=models.RESTRICT)
    issue_to = models.ForeignKey("Issue", related_name="related_from",
            on_delete=models.RESTRICT)
    relation_type = models.CharField(max_length=1024)
    delay = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "issue_relations"
        unique_together = (("issue_from", "issue_to"),)


class IssueStatus(models.Model):
    name = models.CharField(max_length=30)
    is_closed = models.BooleanField()
    position = models.IntegerField(blank=True, null=True)
    default_done_ratio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "issue_statuses"


class Issue(models.Model):
    tracker = models.ForeignKey("Tracker", on_delete=models.RESTRICT)
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)
    subject = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey("IssueCategory", blank=True, null=True,
            on_delete=models.RESTRICT)
    status = models.ForeignKey("IssueStatus", on_delete=models.RESTRICT)
    assigned_to = models.ForeignKey(
        "User",
        related_name="assigned_issues",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    priority = models.ForeignKey("Enumeration", on_delete=models.RESTRICT)
    fixed_version = models.ForeignKey("Version", blank=True, null=True,
            on_delete=models.RESTRICT)
    author = models.ForeignKey("User", on_delete=models.RESTRICT)
    lock_version = models.IntegerField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    done_ratio = models.IntegerField()
    estimated_hours = models.FloatField(blank=True, null=True)
    parent = models.ForeignKey(
        "Issue",
        related_name="children",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    root = models.ForeignKey("Issue", blank=True, null=True, on_delete=models.RESTRICT)
    lft = models.IntegerField(blank=True, null=True)
    rgt = models.IntegerField(blank=True, null=True)
    is_private = models.BooleanField()
    closed_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "issues"


class JournalDetail(models.Model):
    journal = models.ForeignKey("Journal", on_delete=models.RESTRICT)
    property = models.CharField(max_length=30)
    prop_key = models.CharField(max_length=30)
    old_value = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "journal_details"


class Journal(models.Model):
    journalized_id = models.IntegerField()
    journalized_type = models.CharField(max_length=30)
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField()
    private_notes = models.BooleanField()

    class Meta:
        managed = redmine_models_managed
        db_table = "journals"


class MemberRole(models.Model):
    member = models.ForeignKey("Member", on_delete=models.RESTRICT)
    role = models.ForeignKey("Role", on_delete=models.RESTRICT)
    inherited_from = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "member_roles"


class Member(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)
    created_on = models.DateTimeField(blank=True, null=True)
    mail_notification = models.BooleanField()

    class Meta:
        managed = redmine_models_managed
        db_table = "members"
        unique_together = (("user", "project"),)


class Message(models.Model):
    board = models.ForeignKey(Board, on_delete=models.RESTRICT)
    parent = models.ForeignKey("Message", blank=True, null=True, on_delete=models.RESTRICT)
    subject = models.CharField(max_length=1024)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey("User", blank=True, null=True, on_delete=models.RESTRICT)
    replies_count = models.IntegerField()
    last_reply = models.ForeignKey(
        "Message",
        related_name="last_reply_to",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    locked = models.BooleanField(null=True, blank=True)
    sticky = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "messages"


class News(models.Model):
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.RESTRICT)
    title = models.CharField(max_length=60)
    summary = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey("User", on_delete=models.RESTRICT)
    created_on = models.DateTimeField(blank=True, null=True)
    comments_count = models.IntegerField()

    class Meta:
        managed = redmine_models_managed
        db_table = "news"


class OpenIdAuthenticationAssociation(models.Model):
    issued = models.IntegerField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    handle = models.CharField(max_length=1024, blank=True, null=True)
    assoc_type = models.CharField(max_length=1024, blank=True, null=True)
    server_url = models.BinaryField(blank=True, null=True)
    secret = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "open_id_authentication_associations"


class OpenIdAuthenticationNonce(models.Model):
    timestamp = models.IntegerField()
    server_url = models.CharField(max_length=1024, blank=True, null=True)
    salt = models.CharField(max_length=1024)

    class Meta:
        managed = redmine_models_managed
        db_table = "open_id_authentication_nonces"


class Project(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    homepage = models.CharField(max_length=1024, blank=True, null=True)
    is_public = models.BooleanField()
    parent = models.ForeignKey("Project",
        related_name="children",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    identifier = models.CharField(max_length=1024, blank=True, null=True)
    status = models.IntegerField()
    lft = models.IntegerField(blank=True, null=True)
    rgt = models.IntegerField(blank=True, null=True)
    inherit_members = models.BooleanField()
    default_version = models.ForeignKey(
        "Version",
        related_name="projects_with_this_default_version",
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )
    default_assigned_to = models.ForeignKey("User",
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
    )

    class Meta:
        managed = redmine_models_managed
        db_table = "projects"


class ProjectTracker(models.Model):
    project = models.ForeignKey("Project", on_delete=models.RESTRICT)
    tracker = models.ForeignKey("Tracker", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "projects_trackers"
        unique_together = (("project", "tracker"),)


class Query(models.Model):
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024)
    filters = models.TextField(blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    column_names = models.TextField(blank=True, null=True)
    sort_criteria = models.TextField(blank=True, null=True)
    group_by = models.CharField(max_length=1024, blank=True, null=True)
    type = models.CharField(max_length=1024, blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "queries"


class QueryRole(models.Model):
    query = models.ForeignKey(Query, on_delete=models.RESTRICT)
    role = models.ForeignKey("Role", on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "queries_roles"
        unique_together = (("query", "role"),)


class Repository(models.Model):
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    url = models.CharField(max_length=1024)
    login = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=1024, blank=True, null=True)
    root_url = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=1024, blank=True, null=True)
    path_encoding = models.CharField(max_length=64, blank=True, null=True)
    log_encoding = models.CharField(max_length=64, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)
    identifier = models.CharField(max_length=1024, blank=True, null=True)
    is_default = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "repositories"


class Role(models.Model):
    name = models.CharField(max_length=255)
    position = models.IntegerField(blank=True, null=True)
    assignable = models.BooleanField(null=True, blank=True)
    builtin = models.IntegerField()
    permissions = models.TextField(blank=True, null=True)
    issues_visibility = models.CharField(max_length=30)
    users_visibility = models.CharField(max_length=30)
    time_entries_visibility = models.CharField(max_length=30)
    all_roles_managed = models.BooleanField()
    settings = models.TextField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "roles"


class RoleManagedRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    managed_role = models.ForeignKey(Role, related_name="managed_by",
            on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "roles_managed_roles"
        unique_together = (("role", "managed_role"),)


class SchemaMigration(models.Model):
    version = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = redmine_models_managed
        db_table = "schema_migrations"


class Setting(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "settings"


class TimeEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    author = models.ForeignKey("User",
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name='authors',
    )
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    issue = models.ForeignKey(Issue, blank=True, null=True, on_delete=models.RESTRICT)
    hours = models.FloatField()
    comments = models.CharField(max_length=1024, blank=True, null=True)
    activity = models.ForeignKey(Enumeration, on_delete=models.RESTRICT)
    spent_on = models.DateField()
    tyear = models.IntegerField()
    tmonth = models.IntegerField()
    tweek = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    class Meta:
        managed = redmine_models_managed
        db_table = "time_entries"


class Token(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    action = models.CharField(max_length=30)
    value = models.CharField(unique=True, max_length=40)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "tokens"


class Tracker(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    is_in_chlog = models.BooleanField()
    position = models.IntegerField(blank=True, null=True)
    is_in_roadmap = models.BooleanField()
    fields_bits = models.IntegerField(blank=True, null=True)
    default_status = models.ForeignKey(IssueStatus, blank=True, null=True,
            on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "trackers"


class UserPreference(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    others = models.TextField(blank=True, null=True)
    hide_mail = models.BooleanField(null=True, blank=True)
    time_zone = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "user_preferences"


class User(models.Model):
    login = models.CharField(max_length=1024)
    hashed_password = models.CharField(max_length=40)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=255)
    admin = models.BooleanField()
    status = models.IntegerField()
    last_login_on = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)
    auth_source = models.ForeignKey(AuthSource, blank=True, null=True,
            on_delete=models.RESTRICT)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=1024, blank=True, null=True)
    identity_url = models.CharField(max_length=1024, blank=True, null=True)
    mail_notification = models.CharField(max_length=1024)
    salt = models.CharField(max_length=64, blank=True, null=True)
    must_change_passwd = models.BooleanField()
    passwd_changed_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "users"


class Version(models.Model):
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    wiki_page_title = models.CharField(max_length=1024, blank=True, null=True)
    status = models.CharField(max_length=1024, blank=True, null=True)
    sharing = models.CharField(max_length=1024)

    class Meta:
        managed = redmine_models_managed
        db_table = "versions"


class Watcher(models.Model):
    watchable_type = models.CharField(max_length=1024)
    watchable_id = models.IntegerField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "watchers"


class WikiContentVersion(models.Model):
    wiki_content = models.ForeignKey("WikiContent", on_delete=models.RESTRICT)
    page = models.ForeignKey("WikiPage", on_delete=models.RESTRICT)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)
    data = models.BinaryField(blank=True, null=True)
    compression = models.CharField(max_length=6, blank=True, null=True)
    comments = models.CharField(max_length=1024, blank=True, null=True)
    updated_on = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = redmine_models_managed
        db_table = "wiki_content_versions"


class WikiContent(models.Model):
    page = models.ForeignKey("WikiPage", on_delete=models.RESTRICT)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.RESTRICT)
    text = models.TextField(blank=True, null=True)
    comments = models.CharField(max_length=1024, blank=True, null=True)
    updated_on = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = redmine_models_managed
        db_table = "wiki_contents"


class WikiPage(models.Model):
    wiki = models.ForeignKey("Wiki", on_delete=models.RESTRICT)
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField()
    protected = models.BooleanField()
    parent = models.ForeignKey("WikiPage", blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        managed = redmine_models_managed
        db_table = "wiki_pages"


class WikiRedirect(models.Model):
    wiki = models.ForeignKey("Wiki", on_delete=models.RESTRICT)
    title = models.CharField(max_length=1024, blank=True, null=True)
    redirects_to = models.CharField(max_length=1024, blank=True, null=True)
    created_on = models.DateTimeField()
    redirects_to_wiki = models.ForeignKey(
        "Wiki",
        related_name="redirected_from",
        on_delete=models.RESTRICT,
    )

    class Meta:
        managed = redmine_models_managed
        db_table = "wiki_redirects"


class Wiki(models.Model):
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    start_page = models.CharField(max_length=255)
    status = models.IntegerField()

    class Meta:
        managed = redmine_models_managed
        db_table = "wikis"


class Workflow(models.Model):
    tracker = models.ForeignKey(Tracker, on_delete=models.RESTRICT)
    old_status = models.ForeignKey(
        IssueStatus,
        related_name="workflows_where_old",
        on_delete=models.RESTRICT,
    )
    new_status = models.ForeignKey(
        IssueStatus,
        related_name="workflows_where_new",
        on_delete=models.RESTRICT,
    )
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    assignee = models.BooleanField()
    author = models.BooleanField()
    type = models.CharField(max_length=30, blank=True, null=True)
    field_name = models.CharField(max_length=30, blank=True, null=True)
    rule = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = redmine_models_managed
        db_table = "workflows"
