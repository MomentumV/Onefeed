from git import Repo

PATH_OF_GIT_REPO = r'C:\Users\morde\PycharmProjects\Onefeed\.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'update from script'


def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        repo.git.clear_cache()
    except:
        print('Some error occured while pushing the code')
