from jira import JIRA
import os


class WorkFlow:
    def __init__(self):
        """
            271 - Open
            151 - Issue is sprint ready
            161 - Assign to current sprint
            91 - Begin work
            191 - Ready for code review
            201 - Passed code review
            21 - Ready for testing
            241 - Passed testing
            121 - Closed
        """
        self.OPEN = 271
        self.SPRINT_READY = 151
        self.CURRENT_SPRINT = 161
        self.BEGIN_WORK = 91
        self.CODE_REVIEW = 191
        self.INTEGRATION = 201
        self.TEST = 21
        self.VERIFY = 241
        self.CLOSED = 121

        self.__wfo = [
            self.OPEN,
            self.SPRINT_READY,
            self.CURRENT_SPRINT,
            self.BEGIN_WORK,
            self.CODE_REVIEW,
            self.INTEGRATION,
            self.TEST,
            self.VERIFY,
            self.CLOSED
        ]

    def previous(self, n):
        return self.__wfo[self.__wfo.index(n) - 1]

    def next(self, n):
        return self.__wfo[self.__wfo.index(n) + 1]

    def valid(self, n):
        return n in self.__wfo


class AutoJIRA:
    def __init__(self, **kwargs):
        if 'server' in kwargs:
            server = kwargs['server']
        else:
            server = os.environ['JIRA_URL']

        if 'api_user' in kwargs:
            api_user = kwargs['api_user']
        else:
            api_user = os.environ['JIRA_API_USER']

        if 'api_token' in kwargs:
            api_token = kwargs['api_token']
        else:
            api_token = os.environ['JIRA_API_TOKEN']

        self.__jc = JIRA(server=server, basic_auth=(api_user, api_token))
        self.__wf = WorkFlow()

    def __get_issues(self, **kwargs):
        issues = []
        if 'jql' in kwargs:
            issues += self.__jc.search_issues(jql_str=kwargs['jql'])

        if 'key' in kwargs:
            issues += self.__jc.issue(kwargs['key'])

        if 'file' in kwargs:
            with open(kwargs['file']) as fp:
                for key in fp.readlines():
                    issues += self.__jc.issue(key.strip())

        return issues

    def __move(self, issue, n):
        if n not in list(map(lambda x: int(x['id']), self.__jc.transitions(issue))):
            self.__move(issue, self.__wf.previous(n))
        self.__jc.transition_issue(issue, n)

    def move(self, status, **kwargs):
        if self.__wf.valid(status):
            raise ValueError('Not a valid status')

        issues = self.__get_issues(kwargs)

        if len(issues) == 0:
            raise ValueError("No issues to move")

        for issue in issues:
            print('Moving the ticket: {} to {}'.format(issue.key, status))
            self.__move(issue, status)

            if 'comments' in kwargs:
                self.__jc.add_comment(issue, kwargs['comments'])

            if 'assignee' in kwargs:
                self.__jc.assign_issue(issue, kwargs['assignee'])
        print('Done')
