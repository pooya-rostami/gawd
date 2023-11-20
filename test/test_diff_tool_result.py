import pytest

import gawd


def compare_results(first, second):
    """ 
    Compare the two given lists, ignoring item order. 
    
    Not really efficient, but we cannot easily do better, since arbitrary dicts 
    are not hashable nor sortable. 
    """
    for e in first: 
        assert e in second
    for e in second:
        assert e in first
    return True


class TestDiffTool:

    def test_result_1(self):       
        old_workflow = './test/test_cases/test1_old.yaml'
        new_workflow = './test/test_cases/test1_new.yaml'

        expected_result = [('changed', 'jobs.golangci.name', 'Golangci-Lint', 'jobs.golangci.name', 'lint'),
        ('moved', 'jobs.golangci.steps[0]', {'uses': 'actions/checkout@v2'}, 'jobs.golangci.steps[1]', {'uses': 'actions/checkout@v3'}),
        ('changed', 'jobs.golangci.steps[0].uses', 'actions/checkout@v2', 'jobs.golangci.steps[1].uses', 'actions/checkout@v3'),
        ('moved', 'jobs.golangci.steps[1]', {'name': 'Run golangci-lint', 'uses': 'golangci/golangci-lint-action@v2', 'with': {'version': 'v1.40', 'args': '-E gofumpt -E gocritic -E misspell -E revive -E godot'}}, 'jobs.golangci.steps[2]', {'name': 'golangci-lint', 'uses': 'golangci/golangci-lint-action@v3', 'with': {'version': 'v1.45', 'args': '-E gofumpt -E gocritic -E misspell -E revive -E godot'}}),
        ('changed', 'jobs.golangci.steps[1].name', 'Run golangci-lint', 'jobs.golangci.steps[2].name', 'golangci-lint'),
        ('changed', 'jobs.golangci.steps[1].uses', 'golangci/golangci-lint-action@v2', 'jobs.golangci.steps[2].uses', 'golangci/golangci-lint-action@v3'),
        ('changed', 'jobs.golangci.steps[1].with.version', 'v1.40', 'jobs.golangci.steps[2].with.version', 'v1.45'),
        ('added', None, None, 'jobs.golangci.steps[0]', {'uses': 'actions/setup-go@v3'})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_2(self):       
        old_workflow = './test/test_cases/test2_old.yaml'
        new_workflow = './test/test_cases/test2_new.yaml'

        expected_result = [('changed', 'jobs.run.steps[2].run', 'pip install pyfaidx==0.5.8\npython install pytest\n', 'jobs.run.steps[2].run', 'pip install pyfaidx==0.5.8\npip install pytest\n')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_3(self):       
        old_workflow = './test/test_cases/test3_old.yaml'
        new_workflow = './test/test_cases/test3_new.yaml'

        expected_result = [('changed', 'name', 'CodeQL', 'name', 'CodeQL - Code Analysis'),
        ('removed', 'on.pull_request.branches[0]', 'develop', None, None),
        ('added', None, None, 'on.pull_request.branches[0]', '*'),
        ('added', None, None, 'on.pull_request.branches[1]', '*/*'),
        ('renamed', 'jobs.analyse', {'name': 'Analyse', 'runs-on': 'ubuntu-latest', 'steps': [{'name': 'Checkout repository', 'uses': 'actions/checkout@v2', 'with': {'fetch-depth': 2}}, {'run': 'git checkout HEAD^2', 'if': "${{ github.event_name == 'pull_request' }}"}, {'name': 'Initialize CodeQL', 'uses': 'github/codeql-action/init@v1', 'with': {'languages': 'csharp'}}, {'name': 'Autobuild', 'uses': 'github/codeql-action/autobuild@v1'}, {'name': 'Perform CodeQL Analysis', 'uses': 'github/codeql-action/analyze@v1'}]}, 'jobs.analyze', {'name': 'Analyze', 'runs-on': 'ubuntu-latest', 'permissions': {'actions': 'read', 'contents': 'read', 'security-events': 'write'}, 'strategy': {'fail-fast': False, 'matrix': {'language': ['csharp']}}, 'steps': [{'name': 'Checkout repository', 'uses': 'actions/checkout@v3'}, {'name': 'Initialize CodeQL', 'uses': 'github/codeql-action/init@v2', 'with': {'languages': '${{ matrix.language }}'}}, {'name': 'Autobuild', 'uses': 'github/codeql-action/autobuild@v2'}, {'name': 'Perform CodeQL Analysis', 'uses': 'github/codeql-action/analyze@v2'}]}),
        ('added', None, None, 'jobs.analyze.permissions', {'actions': 'read', 'contents': 'read', 'security-events': 'write'}),
        ('added', None, None, 'jobs.analyze.strategy', {'fail-fast': False, 'matrix': {'language': ['csharp']}}),
        ('changed', 'jobs.analyse.name', 'Analyse', 'jobs.analyze.name', 'Analyze'),
        ('moved', 'jobs.analyse.steps[3]', {'name': 'Autobuild', 'uses': 'github/codeql-action/autobuild@v1'}, 'jobs.analyze.steps[2]', {'name': 'Autobuild', 'uses': 'github/codeql-action/autobuild@v2'}),
        ('changed', 'jobs.analyse.steps[3].uses', 'github/codeql-action/autobuild@v1', 'jobs.analyze.steps[2].uses', 'github/codeql-action/autobuild@v2'),
        ('moved', 'jobs.analyse.steps[4]', {'name': 'Perform CodeQL Analysis', 'uses': 'github/codeql-action/analyze@v1'}, 'jobs.analyze.steps[3]', {'name': 'Perform CodeQL Analysis', 'uses': 'github/codeql-action/analyze@v2'}),
        ('changed', 'jobs.analyse.steps[4].uses', 'github/codeql-action/analyze@v1', 'jobs.analyze.steps[3].uses', 'github/codeql-action/analyze@v2'),
        ('moved', 'jobs.analyse.steps[2]', {'name': 'Initialize CodeQL', 'uses': 'github/codeql-action/init@v1', 'with': {'languages': 'csharp'}}, 'jobs.analyze.steps[1]', {'name': 'Initialize CodeQL', 'uses': 'github/codeql-action/init@v2', 'with': {'languages': '${{ matrix.language }}'}}),
        ('changed', 'jobs.analyse.steps[2].uses', 'github/codeql-action/init@v1', 'jobs.analyze.steps[1].uses', 'github/codeql-action/init@v2'),
        ('changed', 'jobs.analyse.steps[2].with.languages', 'csharp', 'jobs.analyze.steps[1].with.languages', '${{ matrix.language }}'),
        ('removed', 'jobs.analyse.steps[0].with', {'fetch-depth': 2}, None, None),
        ('changed', 'jobs.analyse.steps[0].uses', 'actions/checkout@v2', 'jobs.analyze.steps[0].uses', 'actions/checkout@v3'),
        ('removed', 'jobs.analyse.steps[1]', {'run': 'git checkout HEAD^2', 'if': "${{ github.event_name == 'pull_request' }}"}, None, None)]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_4(self):       
        old_workflow = './test/test_cases/test4_old.yaml'
        new_workflow = './test/test_cases/test4_new.yaml'

        expected_result = [('added', None, None, 'on.push.branches[1]', 'auto')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_5(self):       
        old_workflow = './test/test_cases/test5_old.yaml'
        new_workflow = './test/test_cases/test5_new.yaml'

        expected_result = [('changed', 'on.workflow_dispatch.inputs.imageVersion.default', 'v0.3.0', 'on.workflow_dispatch.inputs.imageVersion.default', 'v1.CHANGE_ME')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_6(self):       
        old_workflow = './test/test_cases/test6_old.yaml'
        new_workflow = './test/test_cases/test6_new.yaml'

        expected_result = [('removed', 'on.push.branches[1]', 'master', None, None),
        ('changed', 'jobs.docker_push_dev.if', "${{ github.event_name != 'pull_request' && ( github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master' ) }}", 'jobs.docker_push_dev.if', "${{ github.event_name != 'pull_request' && ( github.ref == 'refs/heads/main' ) }}")]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_7(self):       
        old_workflow = './test/test_cases/test7_old.yaml'
        new_workflow = './test/test_cases/test7_new.yaml'

        expected_result = [('added', None, None, 'jobs.goreleaser.steps[4].name', 'release a new version'),
        ('added', None, None, 'jobs.goreleaser.steps[1].name', 'go-setup'),
        ('added', None, None, 'jobs.goreleaser.steps[3].name', 'goreleaser-setup'),
        ('added', None, None, 'jobs.goreleaser.steps[5].name', 'test releasing a snapshot version'),
        ('added', None, None, 'jobs.goreleaser.steps[0].name', 'checkout'),
        ('added', None, None, 'jobs.goreleaser.steps[2].name', 'install snapcraft')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)


    def test_result_8(self):       
        old_workflow = './test/test_cases/test8_old.yaml'
        new_workflow = './test/test_cases/test8_new.yaml'

        expected_result = [('changed', 'on.push', None, 'on.push', {'branches': ['master', 'main', 'dev/*']}),
        ('changed', 'jobs.linux-build.runs-on', 'ubuntu-20.04', 'jobs.linux-build.runs-on', 'ubuntu-latest')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_9(self):       
        old_workflow = './test/test_cases/test9_old.yaml'
        new_workflow = './test/test_cases/test9_new.yaml'

        expected_result = [('added', None, None, 'on.workflow_dispatch.version.default', '')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_10(self):       
        old_workflow = './test/test_cases/test10_old.yaml'
        new_workflow = './test/test_cases/test10_new.yaml'

        expected_result = [('added', None, None, 'on.pull_request.types[2]', 'synchronize')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_11(self):       
        old_workflow = './test/test_cases/test11_old.yaml'
        new_workflow = './test/test_cases/test11_new.yaml'

        expected_result = [('changed', 'on.push', {'branches': ['*']}, 'on.push', None),
        ('changed', 'jobs.test.steps[0].uses', 'actions/checkout@v2', 'jobs.test.steps[0].uses', 'actions/checkout@v3')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_12(self):       
        old_workflow = './test/test_cases/test12_old.yaml'
        new_workflow = './test/test_cases/test12_new.yaml'

        expected_result = [('changed', 'jobs.analyze.steps[0].uses', 'actions/checkout@v3.1.0', 'jobs.analyze.steps[0].uses', 'actions/checkout@v3.3.0')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_13(self):       
        old_workflow = './test/test_cases/test13_old.yaml'
        new_workflow = './test/test_cases/test13_new.yaml'

        expected_result = [('changed', 'jobs.dependabot-merge.steps[0].uses', 'dependabot/fetch-metadata@v1.3.6', 'jobs.dependabot-merge.steps[0].uses', 'dependabot/fetch-metadata@v1.4.0')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_14(self):       
        old_workflow = './test/test_cases/test14_old.yaml'
        new_workflow = './test/test_cases/test14_new.yaml'

        expected_result = [('changed', 'jobs.analyze.steps[1].uses', 'github/codeql-action/init@v1', 'jobs.analyze.steps[1].uses', 'github/codeql-action/init@v2'),
        ('changed', 'jobs.analyze.steps[2].uses', 'github/codeql-action/autobuild@v1', 'jobs.analyze.steps[2].uses', 'github/codeql-action/autobuild@v2'),
        ('changed', 'jobs.analyze.steps[3].uses', 'github/codeql-action/analyze@v1', 'jobs.analyze.steps[3].uses', 'github/codeql-action/analyze@v2')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_15(self):       
        old_workflow = './test/test_cases/test15_old.yaml'
        new_workflow = './test/test_cases/test15_new.yaml'

        expected_result = [('changed', 'jobs.update_draft_release.steps[0].uses', 'toolmantim/release-drafter@v5.13.0', 'jobs.update_draft_release.steps[0].uses', 'toolmantim/release-drafter@v5.14.0')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_16(self):       
        old_workflow = './test/test_cases/test16_old.yaml'
        new_workflow = './test/test_cases/test16_new.yaml'

        expected_result = [('changed', 'jobs.size.steps[2].uses', 'posva/size-check-action@master', 'jobs.size.steps[2].uses', 'posva/size-check-action@v1.1.0')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_17(self):       
        old_workflow = './test/test_cases/test17_old.yaml'
        new_workflow = './test/test_cases/test17_new.yaml'

        expected_result = [('changed', 'jobs.docs-build.uses', 'rapidsai/shared-action-workflows/.github/workflows/custom-job.yaml@branch-23.04', 'jobs.docs-build.uses', 'rapidsai/shared-action-workflows/.github/workflows/custom-job.yaml@branch-23.06'),
        ('changed', 'jobs.upload-conda.uses', 'rapidsai/shared-action-workflows/.github/workflows/conda-upload-packages.yaml@branch-23.04', 'jobs.upload-conda.uses', 'rapidsai/shared-action-workflows/.github/workflows/conda-upload-packages.yaml@branch-23.06'),
        ('changed', 'jobs.conda-python-build.uses', 'rapidsai/shared-action-workflows/.github/workflows/conda-python-build.yaml@branch-23.04', 'jobs.conda-python-build.uses', 'rapidsai/shared-action-workflows/.github/workflows/conda-python-build.yaml@branch-23.06')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_18(self):       
        old_workflow = './test/test_cases/test18_old.yaml'
        new_workflow = './test/test_cases/test18_new.yaml'

        expected_result = [('renamed', 'jobs.build-latest', {'name': 'Test on Latest', 'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v1'}, {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'stable', 'profile': 'minimal', 'override': True}}, {'name': 'Test', 'run': 'make test'}]}, 'jobs.test-latest', {'name': 'Test on Latest', 'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v1'}, {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'stable', 'profile': 'minimal', 'override': True}}, {'name': 'Test', 'run': 'make test'}]}),
        ('renamed', 'jobs.build-stable', {'name': 'Test on 1.41.0', 'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v1'}, {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': '1.41.0', 'profile': 'minimal', 'override': True}}, {'name': 'Test', 'run': 'make test-141'}]}, 'jobs.test-stable', {'name': 'Test on 1.46.0', 'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v1'}, {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': '1.46.0', 'profile': 'minimal', 'override': True}}, {'name': 'Test', 'run': 'make test'}]}),
        ('changed', 'jobs.build-stable.name', 'Test on 1.41.0', 'jobs.test-stable.name', 'Test on 1.46.0'),
        ('changed', 'jobs.build-stable.steps[1].with.toolchain', '1.41.0', 'jobs.test-stable.steps[1].with.toolchain', '1.46.0'),
        ('changed', 'jobs.build-stable.steps[2].run', 'make test-141', 'jobs.test-stable.steps[2].run', 'make test')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_19(self):       
        old_workflow = './test/test_cases/test19_old.yaml'
        new_workflow = './test/test_cases/test19_new.yaml'

        expected_result = [('renamed', 'jobs.build-compat', {'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'set up JDK 1.8', 'uses': 'actions/setup-java@v1', 'with': {'java-version': 1.8}}, {'name': 'Build and check', 'run': 'cd compat && ./gradlew assembleDebug lintDebug'}, {'name': 'Upload build reports', 'if': 'always()', 'uses': 'actions/upload-artifact@v1', 'with': {'name': 'build-reports', 'path': 'compat/app/build/reports'}}]}, 'jobs.build-all', {'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'set up JDK 1.8', 'uses': 'actions/setup-java@v1', 'with': {'java-version': 1.8}}, {'name': 'Build and check', 'run': 'find . -name "gradlew" -exec ./{} assembleDebug lintDebug \\;'}]}),
        ('changed', 'jobs.build-compat.steps[2].run', 'cd compat && ./gradlew assembleDebug lintDebug', 'jobs.build-all.steps[2].run', 'find . -name "gradlew" -exec ./{} assembleDebug lintDebug \\;'),
        ('removed', 'jobs.build-compat.steps[3]', {'name': 'Upload build reports', 'if': 'always()', 'uses': 'actions/upload-artifact@v1', 'with': {'name': 'build-reports', 'path': 'compat/app/build/reports'}}, None, None),
        ('removed', 'jobs.build-demo-java', {'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'set up JDK 1.8', 'uses': 'actions/setup-java@v1', 'with': {'java-version': 1.8}}, {'name': 'Build and check', 'run': 'cd demo-java && ./gradlew assembleDebug lintDebug'}, {'name': 'Upload build reports', 'if': 'always()', 'uses': 'actions/upload-artifact@v1', 'with': {'name': 'build-reports', 'path': 'demo-java/app/build/reports'}}]}, None, None),
        ('removed', 'jobs.build-demo-kotlin', {'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'set up JDK 1.8', 'uses': 'actions/setup-java@v1', 'with': {'java-version': 1.8}}, {'name': 'Build and check', 'run': 'cd demo-kotlin && ./gradlew assembleDebug lintDebug'}, {'name': 'Upload build reports', 'if': 'always()', 'uses': 'actions/upload-artifact@v1', 'with': {'name': 'build-reports', 'path': 'demo-kotlin/app/build/reports'}}]}, None, None)]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_20(self):       
        old_workflow = './test/test_cases/test20_old.yaml'
        new_workflow = './test/test_cases/test20_new.yaml'

        expected_result = [('renamed', 'jobs.linux-x64', {'name': 'Linux Intel - OpenOCD ${{ github.event.inputs.version }} build', 'timeout-minutes': 5760, 'runs-on': ['self-hosted', 'linux', 'x64'], 'container': {'image': 'ilegeul/ubuntu:amd64-18.04-xbb-v5.0.0'}, 'defaults': {'run': {'shell': 'bash'}}, 'steps': [{'name': 'Environment', 'run': 'uname -a\nlsb_release -sd\necho "whoami: $(whoami)"\necho "pwd: $(pwd)"\necho "node: $(node --version)"\necho "npm: $(npm --version)"\nls -lLA\nenv | sort | egrep \'^[^ \\t]+=\'\n'}, {'name': 'Clean working area', 'run': 'rm -rf * .git*'}, {'name': 'Checkout project', 'uses': 'actions/checkout@v1', 'with': {'fetch-depth': 1}}, {'name': 'Install xpm', 'timeout-minutes': 1440, 'run': 'npm install --location=global xpm@latest'}, {'name': 'Install project dependencies', 'timeout-minutes': 1440, 'run': 'xpm install'}, {'name': 'Build Linux x64 binary', 'timeout-minutes': 1440, 'run': 'xpm install --config linux-x64\nxpm run build --config linux-x64\n'}, {'name': 'Build Windows x64 binary', 'timeout-minutes': 1440, 'run': 'xpm install --config win32-x64\nxpm run build --config win32-x64\n'}, {'name': 'Publish pre-release', 'uses': 'ncipollo/release-action@v1', 'with': {'allowUpdates': True, 'artifacts': 'build/linux-x64/deploy/*,build/win32-x64/deploy/*', 'bodyFile': '.github/workflows/body-github-pre-releases-test.md', 'commit': 'master', 'draft': False, 'name': 'Test binaries', 'omitBodyDuringUpdate': True, 'omitDraftDuringUpdate': True, 'omitNameDuringUpdate': True, 'owner': 'xpack-dev-tools', 'prerelease': True, 'replacesArtifacts': True, 'repo': 'pre-releases', 'tag': 'test', 'token': '${{ secrets.PUBLISH_TOKEN }}'}}, {'name': 'Rename working area', 'run': 'mv -v build build-$(date -u +%Y%m%d-%H%M%S)'}]}, 'jobs.linux-x64-x', {'name': 'Linux Intel X - OpenOCD ${{ github.event.inputs.version }} build', 'timeout-minutes': 5760, 'runs-on': ['self-hosted', 'linux', 'x64'], 'container': {'image': 'ilegeul/ubuntu:amd64-18.04-xbb-v5.0.0'}, 'defaults': {'run': {'shell': 'bash'}}, 'steps': [{'name': 'Environment', 'run': 'uname -a\nlsb_release -sd\necho "whoami: $(whoami)"\necho "pwd: $(pwd)"\necho "node: $(node --version)"\necho "npm: $(npm --version)"\nls -lLA\nenv | sort | egrep \'^[^ \\t]+=\'\n'}, {'name': 'Clean working area', 'run': 'rm -rf * .git*'}, {'name': 'Checkout project', 'uses': 'actions/checkout@v1', 'with': {'fetch-depth': 1}}, {'name': 'Install xpm', 'timeout-minutes': 1440, 'run': 'npm install --location=global xpm@latest'}, {'name': 'Install project dependencies', 'timeout-minutes': 1440, 'run': 'xpm install'}, {'name': 'Build Linux x64 binary', 'timeout-minutes': 1440, 'run': 'xpm install --config linux-x64\nxpm run build --config linux-x64\n'}, {'name': 'Publish pre-release', 'uses': 'ncipollo/release-action@v1', 'with': {'allowUpdates': True, 'artifacts': 'build/linux-x64/deploy/*', 'bodyFile': '.github/workflows/body-github-pre-releases-test.md', 'commit': 'master', 'draft': False, 'name': 'Test binaries', 'omitBodyDuringUpdate': True, 'omitDraftDuringUpdate': True, 'omitNameDuringUpdate': True, 'owner': 'xpack-dev-tools', 'prerelease': True, 'replacesArtifacts': True, 'repo': 'pre-releases', 'tag': 'test', 'token': '${{ secrets.PUBLISH_TOKEN }}'}}, {'name': 'Rename working area', 'run': 'mv -v build build-$(date -u +%Y%m%d-%H%M%S)'}]}),
        ('changed', 'jobs.linux-x64.name', 'Linux Intel - OpenOCD ${{ github.event.inputs.version }} build', 'jobs.linux-x64-x.name', 'Linux Intel X - OpenOCD ${{ github.event.inputs.version }} build'),
        ('moved', 'jobs.linux-x64.steps[8]', {'name': 'Rename working area', 'run': 'mv -v build build-$(date -u +%Y%m%d-%H%M%S)'}, 'jobs.linux-x64-x.steps[7]', {'name': 'Rename working area', 'run': 'mv -v build build-$(date -u +%Y%m%d-%H%M%S)'}),
        ('moved', 'jobs.linux-x64.steps[7]', {'name': 'Publish pre-release', 'uses': 'ncipollo/release-action@v1', 'with': {'allowUpdates': True, 'artifacts': 'build/linux-x64/deploy/*,build/win32-x64/deploy/*', 'bodyFile': '.github/workflows/body-github-pre-releases-test.md', 'commit': 'master', 'draft': False, 'name': 'Test binaries', 'omitBodyDuringUpdate': True, 'omitDraftDuringUpdate': True, 'omitNameDuringUpdate': True, 'owner': 'xpack-dev-tools', 'prerelease': True, 'replacesArtifacts': True, 'repo': 'pre-releases', 'tag': 'test', 'token': '${{ secrets.PUBLISH_TOKEN }}'}}, 'jobs.linux-x64-x.steps[6]', {'name': 'Publish pre-release', 'uses': 'ncipollo/release-action@v1', 'with': {'allowUpdates': True, 'artifacts': 'build/linux-x64/deploy/*', 'bodyFile': '.github/workflows/body-github-pre-releases-test.md', 'commit': 'master', 'draft': False, 'name': 'Test binaries', 'omitBodyDuringUpdate': True, 'omitDraftDuringUpdate': True, 'omitNameDuringUpdate': True, 'owner': 'xpack-dev-tools', 'prerelease': True, 'replacesArtifacts': True, 'repo': 'pre-releases', 'tag': 'test', 'token': '${{ secrets.PUBLISH_TOKEN }}'}}),
        ('changed', 'jobs.linux-x64.steps[7].with.artifacts', 'build/linux-x64/deploy/*,build/win32-x64/deploy/*', 'jobs.linux-x64-x.steps[6].with.artifacts', 'build/linux-x64/deploy/*'),
        ('removed', 'jobs.linux-x64.steps[6]', {'name': 'Build Windows x64 binary', 'timeout-minutes': 1440, 'run': 'xpm install --config win32-x64\nxpm run build --config win32-x64\n'}, None, None),
        ('added', None, None, 'jobs.linux-x64-w', {'name': 'Linux Intel W - OpenOCD ${{ github.event.inputs.version }} build', 'timeout-minutes': 5760, 'runs-on': ['self-hosted', 'linux', 'x64'], 'container': {'image': 'ilegeul/ubuntu:amd64-18.04-xbb-v5.0.0'}, 'defaults': {'run': {'shell': 'bash'}}, 'steps': [{'name': 'Environment', 'run': 'uname -a\nlsb_release -sd\necho "whoami: $(whoami)"\necho "pwd: $(pwd)"\necho "node: $(node --version)"\necho "npm: $(npm --version)"\nls -lLA\nenv | sort | egrep \'^[^ \\t]+=\'\n'}, {'name': 'Clean working area', 'run': 'rm -rf * .git*'}, {'name': 'Checkout project', 'uses': 'actions/checkout@v1', 'with': {'fetch-depth': 1}}, {'name': 'Install xpm', 'timeout-minutes': 1440, 'run': 'npm install --location=global xpm@latest'}, {'name': 'Install project dependencies', 'timeout-minutes': 1440, 'run': 'xpm install'}, {'name': 'Build Windows x64 binary', 'timeout-minutes': 1440, 'run': 'xpm install --config win32-x64\nxpm run build --config win32-x64\n'}, {'name': 'Publish pre-release', 'uses': 'ncipollo/release-action@v1', 'with': {'allowUpdates': True, 'artifacts': 'build/win32-x64/deploy/*', 'bodyFile': '.github/workflows/body-github-pre-releases-test.md', 'commit': 'master', 'draft': False, 'name': 'Test binaries', 'omitBodyDuringUpdate': True, 'omitDraftDuringUpdate': True, 'omitNameDuringUpdate': True, 'owner': 'xpack-dev-tools', 'prerelease': True, 'replacesArtifacts': True, 'repo': 'pre-releases', 'tag': 'test', 'token': '${{ secrets.PUBLISH_TOKEN }}'}}, {'name': 'Rename working area', 'run': 'mv -v build build-$(date -u +%Y%m%d-%H%M%S)'}]})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_21(self):       
        old_workflow = './test/test_cases/test21_old.yaml'
        new_workflow = './test/test_cases/test21_new.yaml'

        expected_result = [('changed', 'jobs.build-linux-clangpdb-gcc5.steps[1].run', 'sudo apt-get update\nsudo apt-get install nasm uuid-dev libssl-dev iasl\nfile="clang+llvm-13.0.0-x86_64-linux-gnu-ubuntu-20.04"\nsuf=".tar.xz"\ncurl -LO "https://github.com/llvm/llvm-project/releases/download/llvmorg-13.0.0/${file}${suf}" || exit 1\nsum=$(shasum -a 256 "${file}${suf}" | cut -f1 -d\' \')\nexpsum="2c2fb857af97f41a5032e9ecadf7f78d3eff389a5cd3c9ec620d24f134ceb3c8"\nif [ "$sum" != "$expsum" ]; then echo "Invalid checksum $sum" ; exit 1 ; fi\ntar -xf "${file}${suf}" || exit 1\necho "$(pwd)/${file}/bin" >> $GITHUB_PATH\n', 'jobs.build-linux-clangpdb-gcc5.steps[1].run', 'sudo apt-get update\nsudo apt-get install nasm uuid-dev libssl-dev iasl\nwget https://apt.llvm.org/llvm.sh\nchmod +x llvm.sh\nsudo ./llvm.sh 13\necho "/usr/lib/llvm-13/bin" >> $GITHUB_PATH\n'),
        ('renamed', 'jobs.build-linux-clang38', {'name': 'Build Linux CLANG38', 'runs-on': 'ubuntu-latest', 'env': {'TOOLCHAINS': 'CLANG38'}, 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'Install Dependencies', 'run': 'sudo apt-get update\nsudo apt-get install nasm uuid-dev iasl doxygen texlive texlive-latex-extra\nwget https://apt.llvm.org/llvm.sh\nchmod +x llvm.sh\nsudo ./llvm.sh 13\necho "/usr/lib/llvm-13/bin" >> $GITHUB_PATH\n'}, {'name': 'CI Bootstrap', 'run': 'src=$(/usr/bin/curl -Lfs https://raw.githubusercontent.com/acidanthera/ocbuild/master/ci-bootstrap.sh) && eval "$src" || exit 1\n'}, {'run': './build_duet.tool'}, {'run': './build_oc.tool'}, {'name': 'Build Docs', 'run': 'abort() { tail -200 log.txt ; exit 1 ; }\ndoxygen Doxyfile &> log.txt || abort\ncd Doxy/latex || abort\nmake pdf &> log.txt || abort\n'}, {'name': 'Upload to Artifacts', 'uses': 'actions/upload-artifact@v2', 'with': {'name': 'Linux CLANG38 Artifacts', 'path': 'Binaries/*.zip'}}]}, 'jobs.build-linux-clangdwarf', {'name': 'Build Linux CLANGDWARF', 'runs-on': 'ubuntu-latest', 'env': {'TOOLCHAINS': 'CLANGDWARF'}, 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'Install Dependencies', 'run': 'sudo apt-get update\nsudo apt-get install nasm uuid-dev iasl doxygen texlive texlive-latex-extra\nwget https://apt.llvm.org/llvm.sh\nchmod +x llvm.sh\nsudo ./llvm.sh 13\necho "/usr/lib/llvm-13/bin" >> $GITHUB_PATH\n'}, {'name': 'CI Bootstrap', 'run': 'src=$(/usr/bin/curl -Lfs https://raw.githubusercontent.com/acidanthera/ocbuild/master/ci-bootstrap.sh) && eval "$src" || exit 1\n'}, {'run': './build_duet.tool'}, {'run': './build_oc.tool'}, {'name': 'Build Docs', 'run': 'abort() { tail -200 log.txt ; exit 1 ; }\ndoxygen Doxyfile &> log.txt || abort\ncd Doxy/latex || abort\nmake pdf &> log.txt || abort\n'}, {'name': 'Upload to Artifacts', 'uses': 'actions/upload-artifact@v2', 'with': {'name': 'Linux CLANGDWARF Artifacts', 'path': 'Binaries/*.zip'}}]}),
        ('changed', 'jobs.build-linux-clang38.name', 'Build Linux CLANG38', 'jobs.build-linux-clangdwarf.name', 'Build Linux CLANGDWARF'),
        ('changed', 'jobs.build-linux-clang38.env.TOOLCHAINS', 'CLANG38', 'jobs.build-linux-clangdwarf.env.TOOLCHAINS', 'CLANGDWARF'),
        ('changed', 'jobs.build-linux-clang38.steps[6].with.name', 'Linux CLANG38 Artifacts', 'jobs.build-linux-clangdwarf.steps[6].with.name', 'Linux CLANGDWARF Artifacts')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_22(self):       
        old_workflow = './test/test_cases/test22_old.yaml'
        new_workflow = './test/test_cases/test22_new.yaml'

        expected_result = [('renamed', 'jobs.github-actions-automate-projects', {'runs-on': 'ubuntu-latest', 'steps': [{'name': 'add-new-issues-to-repository-based-project-column', 'uses': 'docker://takanabe/github-actions-automate-projects:v0.0.1', 'if': "github.event_name == 'issues' && github.event.action == 'opened'", 'env': {'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}', 'GITHUB_PROJECT_URL': 'https://github.com/trezor/trezor-firmware/projects/1', 'GITHUB_PROJECT_COLUMN_NAME': '📥 Inbox'}}, {'name': 'add-new-prs-to-repository-based-project-column', 'uses': 'docker://takanabe/github-actions-automate-projects:v0.0.1', 'if': "github.event_name == 'pull_request' && github.event.action == 'opened'", 'env': {'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}', 'GITHUB_PROJECT_URL': 'https://github.com/trezor/trezor-firmware/projects/2', 'GITHUB_PROJECT_COLUMN_NAME': 'To be reviewed'}}]}, 'jobs.gh-automate-projects', {'runs-on': 'ubuntu-latest', 'steps': [{'name': 'Add new issue to the Backlog 🗂  project board', 'if': "github.event_name == 'issues' && github.event.action == 'opened'", 'run': 'gh issue edit $ISSUE --add-project "Backlog 🗂  "', 'env': {'ISSUE': '${{github.event.issue.html_url}}', 'GITHUB_TOKEN': '${{ secrets.GH_BOT_TOKEN }}'}}, {'name': 'Add new pull request to the Pull Requests project board', 'if': "github.event_name == 'pull_request' && github.event.action == 'opened'", 'run': 'gh pr edit $PULL_REQUEST --add-project "Pull Requests"', 'env': {'PULL_REQUEST': '${{github.event.pull_request.html_url}}', 'GITHUB_TOKEN': '${{ secrets.GH_BOT_TOKEN }}'}}]}),
        ('removed', 'jobs.github-actions-automate-projects.steps[0]', {'name': 'add-new-issues-to-repository-based-project-column', 'uses': 'docker://takanabe/github-actions-automate-projects:v0.0.1', 'if': "github.event_name == 'issues' && github.event.action == 'opened'", 'env': {'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}', 'GITHUB_PROJECT_URL': 'https://github.com/trezor/trezor-firmware/projects/1', 'GITHUB_PROJECT_COLUMN_NAME': '📥 Inbox'}}, None, None),
        ('removed', 'jobs.github-actions-automate-projects.steps[1]', {'name': 'add-new-prs-to-repository-based-project-column', 'uses': 'docker://takanabe/github-actions-automate-projects:v0.0.1', 'if': "github.event_name == 'pull_request' && github.event.action == 'opened'", 'env': {'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}', 'GITHUB_PROJECT_URL': 'https://github.com/trezor/trezor-firmware/projects/2', 'GITHUB_PROJECT_COLUMN_NAME': 'To be reviewed'}}, None, None),
        ('added', None, None, 'jobs.gh-automate-projects.steps[0]', {'name': 'Add new issue to the Backlog 🗂  project board', 'if': "github.event_name == 'issues' && github.event.action == 'opened'", 'run': 'gh issue edit $ISSUE --add-project "Backlog 🗂  "', 'env': {'ISSUE': '${{github.event.issue.html_url}}', 'GITHUB_TOKEN': '${{ secrets.GH_BOT_TOKEN }}'}}),
        ('added', None, None, 'jobs.gh-automate-projects.steps[1]', {'name': 'Add new pull request to the Pull Requests project board', 'if': "github.event_name == 'pull_request' && github.event.action == 'opened'", 'run': 'gh pr edit $PULL_REQUEST --add-project "Pull Requests"', 'env': {'PULL_REQUEST': '${{github.event.pull_request.html_url}}', 'GITHUB_TOKEN': '${{ secrets.GH_BOT_TOKEN }}'}})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_23(self):       
        old_workflow = './test/test_cases/test23_old.yaml'
        new_workflow = './test/test_cases/test23_new.yaml'

        expected_result = [('changed', 'name', 'Test Python aswfdocker Library - Sonar', 'name', 'Test Python aswfdocker Library'), ('removed', 'on.pull_request', {'types': ['opened',        'synchronize', 'reopened']}, None, None), ('changed', 'on.push', {'branches': ['master']}, 'on.push', None), ('changed', 'jobs.release.steps[4].run', 'pipenv run pytest python/aswfdocker --doctest-modules --junitxml=test-pytest-results.xml --cov=. --cov-report=xml', 'jobs.release.steps[4].run', 'pipenv run pre-commit run --all-files'), ('changed', 'jobs.release.steps[4].name', 'Run pytest', 'jobs.release.steps[4].name', 'Run all pre-commit tests'), ('removed', 'jobs.release.steps[5]', {'run': 'pipenv run mypy python/aswfdocker --junit-xml=test-mypy-results.xml', 'name': 'Run mypy'}, None, None), ('removed', 'jobs.release.steps[6]', {'run': 'pipenv run prospector -F python/aswfdocker --output-format xunit > test-prospector-results.xml', 'name': 'Run prospector linter'}, None, None), ('removed', 'jobs.release.steps[7]', {'run': 'pipenv run black python --check', 'name': 'Run black checker'}, None, None), ('removed', 'jobs.release.steps[8]', {'name': 'SonarCloud Scan', 'uses': 'sonarsource/sonarcloud-github-action@master', 'env': {'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}', 'SONAR_TOKEN': '${{ secrets.SONAR_TOKEN }}'}}, None, None)]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_24(self):       
        old_workflow = './test/test_cases/test24_old.yaml'
        new_workflow = './test/test_cases/test24_new.yaml'

        expected_result = [('renamed', 'jobs.test-alpine', {'runs-on': 'ubuntu-latest', 'container': 'alpine:latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'make', 'run': "apk add build-base\nmake REDIS_CFLAGS='-Werror'\n"}, {'name': 'test', 'run': 'apk add tcl procps\n./runtest --accurate --verbose --dump-logs\n'}, {'name': 'module api test', 'run': './runtest-moduleapi --verbose'}, {'name': 'sentinel tests', 'run': './runtest-sentinel'}, {'name': 'cluster tests', 'run': './runtest-cluster'}]}, 'jobs.test-alpine-jemalloc', {'runs-on': 'ubuntu-latest', 'container': 'alpine:latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'make', 'run': "apk add build-base\nmake REDIS_CFLAGS='-Werror'\n"}, {'name': 'test', 'run': 'apk add tcl procps\n./runtest --accurate --verbose --dump-logs\n'}, {'name': 'module api test', 'run': './runtest-moduleapi --verbose'}, {'name': 'sentinel tests', 'run': './runtest-sentinel'}, {'name': 'cluster tests', 'run': './runtest-cluster'}]}), ('added', None, None, 'jobs.test-alpine-libc-malloc', {'runs-on': 'ubuntu-latest', 'container': 'alpine:latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'make', 'run': "apk add build-base\nmake REDIS_CFLAGS='-Werror' USE_JEMALLOC=no\n"}, {'name': 'test', 'run': 'apk add tcl procps\n./runtest --accurate --verbose --dump-logs\n'}, {'name': 'module api test', 'run': './runtest-moduleapi --verbose'}, {'name': 'sentinel tests', 'run': './runtest-sentinel'}, {'name': 'cluster tests', 'run': './runtest-cluster'}]})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_25(self):       
        old_workflow = './test/test_cases/test25_old.yaml'
        new_workflow = './test/test_cases/test25_new.yaml'

        expected_result = [('added', None, None, 'env', {'ARKOUDA_DEVELOPER': True, 'CHPL_RT_OVERSUBSCRIBED': 'yes'}), ('renamed', 'jobs.lint_job', {'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v1'}, {'name': 'look for tabs', 'run': "! git --no-pager grep -n $'\\t' -- '*.chpl'\n"}]}, 'jobs.lint', {'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'Check for tabs', 'run': "! git --no-pager grep -n $'\\t' -- '*.chpl'\n"}]}), ('changed', 'jobs.lint_job.steps[0].uses', 'actions/checkout@v1', 'jobs.lint.steps[0].uses', 'actions/checkout@v2'), ('changed', 'jobs.lint_job.steps[1].name', 'look for tabs', 'jobs.lint.steps[1].name', 'Check for tabs'), ('renamed', 'jobs.linux_job', {'runs-on': 'ubuntu-latest', 'container': {'image': 'chapel/chapel:1.20.0'}, 'steps': [{'uses': 'actions/checkout@v1'}, {'name': 'linux comm=none', 'run': 'apt-get update && apt-get install -y libhdf5-dev libzmq3-dev python3-pip\necho "\\$(eval \\$(call add-path,/usr/lib/x86_64-linux-gnu/hdf5/serial/))" > Makefile.paths\nARKOUDA_DEVELOPER=true make\npip3 install -e .\nmake check\n'}]}, 'jobs.arkouda_tests_linux', {'runs-on': 'ubuntu-latest', 'container': {'image': 'chapel/chapel:1.20.0'}, 'steps': [{'uses': 'actions/checkout@v2'}, {'name': 'Install dependencies', 'run': 'apt-get update && apt-get install -y libhdf5-dev libzmq3-dev python3-pip\necho "\\$(eval \\$(call add-path,/usr/lib/x86_64-linux-gnu/hdf5/serial/))" > Makefile.paths\n'}, {'name': 'Build/Install Arkouda', 'run': 'make\npip3 install -e .\n'}, {'name': 'Arkouda make check', 'run': 'make check\n'}]}), ('changed', 'jobs.linux_job.steps[0].uses', 'actions/checkout@v1', 'jobs.arkouda_tests_linux.steps[0].uses', 'actions/checkout@v2'), ('changed', 'jobs.linux_job.steps[1].name', 'linux comm=none', 'jobs.arkouda_tests_linux.steps[1].name', 'Install dependencies'), ('changed', 'jobs.linux_job.steps[1].run', 'apt-get update && apt-get install -y libhdf5-dev libzmq3-dev python3-pip\necho "\\$(eval \\$(call add-path,/usr/lib/x86_64-linux-gnu/hdf5/serial/))" > Makefile.paths\nARKOUDA_DEVELOPER=true make\npip3 install -e .\nmake check\n', 'jobs.arkouda_tests_linux.steps[1].run', 'apt-get update && apt-get install -y libhdf5-dev libzmq3-dev python3-pip\necho "\\$(eval \\$(call add-path,/usr/lib/x86_64-linux-gnu/hdf5/serial/))" > Makefile.paths\n'), ('added', None, None, 'jobs.arkouda_tests_linux.steps[2]', {'name': 'Build/Install Arkouda', 'run': 'make\npip3 install -e .\n'}), ('added', None, None, 'jobs.arkouda_tests_linux.steps[3]', {'name': 'Arkouda make check', 'run': 'make check\n'})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_26(self):       
        old_workflow = './test/test_cases/test26_old.yaml'
        new_workflow = './test/test_cases/test26_new.yaml'

        expected_result = [('renamed', 'jobs.upgrade-kuma', {'runs-on': 'ubuntu-latest', 'defaults': {'run': {'working-directory': 'kong-mesh'}}, 'steps': [{'name': 'Generate GitHub app token', 'id': 'github-app-token', 'uses': 'tibdex/github-app-token@f717b5ecd4534d3c4df4ce9b5c1c2214f0f7cd06', 'with': {'app_id': '${{ secrets.APP_ID }}', 'private_key': '${{ secrets.APP_PRIVATE_KEY }}'}}, {'name': 'Clone Kuma', 'uses': 'actions/checkout@v2'}, {'uses': 'actions/setup-go@v2', 'with': {'go-version': '~1.18.1'}}, {'run': 'go run ./tools/releases/changelog/... changelog.md > CHANGELOG.md\n'}, {'name': 'Create Pull Request', 'uses': 'peter-evans/create-pull-request@v3', 'with': {'commit-message': 'docs(CHANGELOG.md): Updating changelog', 'signoff': True, 'branch': 'chore/update-changelog', 'delete-branch': True, 'title': 'docs(CHANGELOG.md): Updating changelog', 'draft': False, 'token': '${{ steps.github-app-token.outputs.token }}', 'committer': 'kumahq[bot] <110050114+kumahq[bot]@users.noreply.github.com>', 'author': 'kumahq[bot] <110050114+kumahq[bot]@users.noreply.github.com>'}}]}, 'jobs.update-changelog', {'runs-on': 'ubuntu-latest', 'steps': [{'name': 'Generate GitHub app token', 'id': 'github-app-token', 'uses': 'tibdex/github-app-token@f717b5ecd4534d3c4df4ce9b5c1c2214f0f7cd06', 'with': {'app_id': '${{ secrets.APP_ID }}', 'private_key': '${{ secrets.APP_PRIVATE_KEY }}'}}, {'name': 'Clone Kuma', 'uses': 'actions/checkout@v2'}, {'uses': 'actions/setup-go@v2', 'with': {'go-version': '~1.18.1'}}, {'env': {'GITHUB_TOKEN': '${{ steps.github-app-token.outputs.token }}'}, 'run': 'go run ./tools/releases/changelog/... changelog.md > CHANGELOG.md\n'}, {'name': 'Create Pull Request', 'uses': 'peter-evans/create-pull-request@v3', 'with': {'commit-message': 'docs(CHANGELOG.md): Updating changelog', 'signoff': True, 'branch': 'chore/update-changelog', 'delete-branch': True, 'title': 'docs(CHANGELOG.md): Updating changelog', 'draft': False, 'token': '${{ steps.github-app-token.outputs.token }}', 'committer': 'kumahq[bot] <110050114+kumahq[bot]@users.noreply.github.com>', 'author': 'kumahq[bot] <110050114+kumahq[bot]@users.noreply.github.com>'}}]}), ('removed', 'jobs.upgrade-kuma.defaults', {'run': {'working-directory': 'kong-mesh'}}, None, None), ('added', None, None, 'jobs.update-changelog.steps[3].env', {'GITHUB_TOKEN': '${{ steps.github-app-token.outputs.token }}'})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_27(self):       
        old_workflow = './test/test_cases/test27_old.yaml'
        new_workflow = './test/test_cases/test27_new.yaml'

        expected_result = [('renamed', 'jobs.test', {'runs-on': 'quadcore', 'timeout-minutes': 60, 'steps': [{'uses': 'actions/checkout@v1'}, {'name': 'make', 'run': 'sudo apt-get -y install uuid-dev libcurl4-openssl-dev\nmake -j8\n'}, {'name': 'test 20x', 'run': 'sudo apt-get install tcl8.5\n./runtest --loopn 20\n'}]}, 'jobs.test-endurance', {'runs-on': 'quadcore', 'timeout-minutes': 60, 'steps': [{'uses': 'actions/checkout@v1'}, {'name': 'make', 'run': 'sudo apt-get -y install uuid-dev libcurl4-openssl-dev\nmake -j8\n'}, {'name': 'test 20x', 'run': 'sudo apt-get install tcl8.5\n./runtest --loopn 20 --clients 10\n'}]}), ('changed', 'jobs.test.steps[2].run', 'sudo apt-get install tcl8.5\n./runtest --loopn 20\n', 'jobs.test-endurance.steps[2].run', 'sudo apt-get install tcl8.5\n./runtest --loopn 20 --clients 10\n')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_28(self):       
        old_workflow = './test/test_cases/test28_old.yaml'
        new_workflow = './test/test_cases/test28_new.yaml'

        expected_result = [('removed', 'jobs.gateway.steps[2]', {'name': 'Get dependencies', 'run': 'cd gateway && go get -v -t -d ./...\nif [ -f Gopkg.toml ]; then\n    curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh\n    dep ensure\nfi\n'}, None, None), ('added', None, None, 'jobs.gateway.steps[2]', {'name': 'Cache Go Modules', 'uses': 'actions/cache@v1', 'with': {'path': '~/go/pkg/mod', 'key': "${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}", 'restore-keys': '${{ runner.os }}-go-\n'}}), ('removed', 'jobs.runner.steps[2]', {'name': 'Get dependencies', 'run': 'cd runner && go get -v -t -d ./...\nif [ -f Gopkg.toml ]; then\n    curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh\n    dep ensure\nfi\n'}, None, None), ('added', None, None, 'jobs.runner.steps[2]', {'name': 'Cache Go Modules', 'uses': 'actions/cache@v1', 'with': {'path': '~/go/pkg/mod', 'key': "${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}", 'restore-keys': '${{ runner.os }}-go-\n'}}), ('removed', 'jobs.metric.steps[2]', {'name': 'Get dependencies', 'run': 'cd metric-proxy && go get -v -t -d ./...\nif [ -f Gopkg.toml ]; then\n    curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh\n    dep ensure\nfi\n'}, None, None), ('added', None, None, 'jobs.metric.steps[2]', {'name': 'Cache Go Modules', 'uses': 'actions/cache@v1', 'with': {'path': '~/go/pkg/mod', 'key': "${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}", 'restore-keys': '${{ runner.os }}-go-\n'}}), ('added', None, None, 'jobs.cli', {'name': 'Build and test space cli', 'runs-on': 'ubuntu-latest', 'steps': [{'name': 'Set up Go 1.13', 'uses': 'actions/setup-go@v1', 'with': {'go-version': 1.13}, 'id': 'go'}, {'name': 'Check out code into the Go module directory', 'uses': 'actions/checkout@v1'}, {'name': 'Cache Go Modules', 'uses': 'actions/cache@v1', 'with': {'path': '~/go/pkg/mod', 'key': "${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}", 'restore-keys': '${{ runner.os }}-go-\n'}}, {'name': 'Build', 'run': 'cd space-cli && go build -v .'}, {'name': 'Test', 'run': 'cd space-cli && go test ./...'}, {'name': 'Lint', 'run': 'curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh | sh -s latest\nsudo cp ./bin/golangci-lint $GOPATH/bin/\ncd space-cli && golangci-lint run -E golint --exclude-use-default=false ./...\n'}]})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_29(self):       
        old_workflow = './test/test_cases/test29_old.yaml'
        new_workflow = './test/test_cases/test29_new.yaml'

        expected_result = [('moved', 'jobs.build.steps[1]', {'name': 'Set up Java 8', 'uses': 'actions/setup-java@v3', 'with': {'java-version': 8, 'distribution': 'temurin', 'cache': 'maven'}}, 'jobs.build.steps[2]', {'name': 'Set up Java 8', 'uses': 'actions/setup-java@v3', 'with': {'java-version': 8, 'distribution': 'temurin', 'cache': 'gradle'}}), ('changed', 'jobs.build.steps[1].with.cache', 'maven', 'jobs.build.steps[2].with.cache', 'gradle'), ('moved', 'jobs.build.steps[2]', {'name': 'Build library with Maven', 'run': 'mvn -B verify'}, 'jobs.build.steps[3]', {'name': 'Build libraries with Gradle', 'run': './gradlew clean build'}), ('changed', 'jobs.build.steps[2].name', 'Build library with Maven', 'jobs.build.steps[3].name', 'Build libraries with Gradle'), ('changed', 'jobs.build.steps[2].run', 'mvn -B verify', 'jobs.build.steps[3].run', './gradlew clean build'), ('added', None, None, 'jobs.build.steps[1]', {'name': 'Validate Gradle wrapper', 'uses': 'gradle/wrapper-validation-action@v1'}), ('added', None, None, 'jobs.build.steps[4]', {'name': 'Archive failure build reports', 'uses': 'actions/upload-artifact@v3', 'if': 'failure()', 'with': {'name': 'build-reports', 'path': './**/build/reports\n', 'retention-days': 7}})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_30(self):       
        old_workflow = './test/test_cases/test30_old.yaml'
        new_workflow = './test/test_cases/test30_new.yaml'

        expected_result = [('removed', 'on.push', None, None, None), ('added', None, None, 'on.pull_request', None), ('changed', 'jobs.build.steps[0].name', 'Set up Go 1.13', 'jobs.build.steps[0].name', 'Set up Go 1.12'), ('changed', 'jobs.build.steps[0].with.go-version', 1.13, 'jobs.build.steps[0].with.go-version', 1.12), ('removed', 'jobs.build.steps[2]', {'name': 'Get dependencies', 'run': 'go get -v -t -d ./...\nif [ -f Gopkg.toml ]; then\n    curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh\n    dep ensure\nfi\n'}, None, None), ('removed', 'jobs.build.steps[3]', {'name': 'Build', 'run': 'go build -v .'}, None, None), ('added', None, None, 'jobs.build.steps[2]', {'name': 'Test', 'run': './docker-ci.sh\n'})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_31(self):       
        old_workflow = './test/test_cases/test31_old.yaml'
        new_workflow = './test/test_cases/test31_new.yaml'

        expected_result = [('removed', 'env.MSRV', '1.49.0', None, None), ('removed', 'env.APPENDER_MSRV', '1.53.0', None, None), ('removed', 'jobs.test-features-stable.steps[1]', {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'stable', 'profile': 'minimal', 'override': True}}, None, None), ('added', None, None, 'jobs.test-features-stable.steps[1]', {'uses': 'dtolnay/rust-toolchain@stable'}), ('removed', 'jobs.test.steps[1]', {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': '${{ matrix.rust }}', 'profile': 'minimal', 'override': True}}, None, None), ('added', None, None, 'jobs.test.steps[1]', {'name': 'install Rust ${{ matrix.rust }}', 'uses': 'dtolnay/rust-toolchain@master', 'with': {'toolchain': '${{ matrix.rust }}'}}), ('changed', 'jobs.test-wasm.steps[1].uses', 'actions-rs/toolchain@v1', 'jobs.test-wasm.steps[1].uses', 'dtolnay/rust-toolchain@stable'), ('removed', 'jobs.test-wasm.steps[1].with.toolchain', 'stable', None, None), ('removed', 'jobs.test-wasm.steps[1].with.override', True, None, None), ('removed', 'jobs.cargo-hack.steps[1]', {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'stable', 'profile': 'minimal', 'override': True}}, None, None), ('added', None, None, 'jobs.cargo-hack.steps[1]', {'uses': 'dtolnay/rust-toolchain@stable'}), ('changed', 'jobs.warnings.steps[1].uses', 'actions-rs/toolchain@v1', 'jobs.warnings.steps[1].uses', 'dtolnay/rust-toolchain@stable'), ('removed', 'jobs.warnings.steps[1].with.toolchain', 'stable', None, None), ('removed', 'jobs.warnings.steps[1].with.profile', 'minimal', None, None), ('moved', 'jobs.all_required.needs[2]', 'cargo-hack', 'jobs.all_required.needs[1]', 'cargo-hack'), ('moved', 'jobs.all_required.needs[3]', 'check-msrv', 'jobs.all_required.needs[2]', 'check-msrv'), ('moved', 'jobs.all_required.needs[5]', 'test-build-wasm', 'jobs.all_required.needs[3]', 'test-build-wasm'), ('moved', 'jobs.all_required.needs[6]', 'test-wasm', 'jobs.all_required.needs[4]', 'test-wasm'), ('moved', 'jobs.all_required.needs[7]', 'test-features-stable', 'jobs.all_required.needs[5]', 'test-features-stable'), ('removed', 'jobs.all_required.needs[1]', 'minimal-versions', None, None), ('removed', 'jobs.all_required.needs[4]', 'check-msrv-appender', None, None), ('changed', 'jobs.test-build-wasm.steps[1].uses', 'actions-rs/toolchain@v1', 'jobs.test-build-wasm.steps[1].uses', 'dtolnay/rust-toolchain@stable'), ('removed', 'jobs.test-build-wasm.steps[1].with.toolchain', 'stable', None, None), ('removed', 'jobs.test-build-wasm.steps[1].with.override', True, None, None), ('removed', 'jobs.test-build-wasm.steps[2]', {'name': 'build all tests', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'test', 'args': '--no-run -p ${{ matrix.subcrate }}'}}, None, None), ('added', None, None, 'jobs.test-build-wasm.steps[2]', {'name': 'build all tests', 'run': 'cargo test --no-run -p ${{ matrix.subcrate }}'}), ('changed', 'jobs.style.steps[1].uses', 'actions-rs/toolchain@v1', 'jobs.style.steps[1].uses', 'dtolnay/rust-toolchain@stable'), ('removed', 'jobs.style.steps[1].with.toolchain', 'stable', None, None), ('removed', 'jobs.style.steps[1].with.profile', 'minimal', None, None), ('removed', 'jobs.style.steps[1].with.override', True, None, None), ('removed', 'jobs.style.steps[2]', {'name': 'rustfmt', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'fmt', 'args': '--all -- --check'}}, None, None), ('added', None, None, 'jobs.style.steps[2]', {'name': 'rustfmt', 'run': 'cargo fmt --all -- --check'}), ('removed', 'jobs.check.steps[1]', {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'stable', 'profile': 'minimal', 'override': True}}, None, None), ('removed', 'jobs.check.steps[2]', {'name': 'Check', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'check', 'args': '--all --tests --benches'}}, None, None), ('added', None, None, 'jobs.check.steps[1]', {'uses': 'dtolnay/rust-toolchain@stable'}), ('added', None, None, 'jobs.check.steps[2]', {'name': 'Check', 'run': 'cargo check --all --tests --benches'}), ('added', None, None, 'jobs.check-msrv.strategy', {'matrix': {'subcrate': ['tracing-attributes', 'tracing-core', 'tracing-futures', 'tracing-log', 'tracing-macros', 'tracing-serde', 'tracing-tower', 'tracing-opentelemetry', 'tracing', 'tracing-subscriber'], 'toolchain': ['1.49.0', 'stable'], 'exclude': [{'subcrate': 'tracing-appender', 'toolchain': '1.49.0'}], 'include': [{'subcrate': 'tracing-appender', 'toolchain': '1.53.0'}]}}), ('changed', 'jobs.check-msrv.name', 'cargo check (MSRV on ubuntu-latest)', 'jobs.check-msrv.name', 'cargo check (+MSRV -Zminimal-versions)'), ('moved', 'jobs.check-msrv.steps[2]', {'name': 'install Rust nightly', 'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'nightly', 'profile': 'minimal'}}, 'jobs.check-msrv.steps[1]', {'name': 'install Rust nightly', 'uses': 'dtolnay/rust-toolchain@nightly'}), ('removed', 'jobs.check-msrv.steps[2].with', {'toolchain': 'nightly', 'profile': 'minimal'}, None, None), ('changed', 'jobs.check-msrv.steps[2].uses', 'actions-rs/toolchain@v1', 'jobs.check-msrv.steps[1].uses', 'dtolnay/rust-toolchain@nightly'), ('moved', 'jobs.check-msrv.steps[1]', {'name': 'install Rust ${{ env.MSRV }}', 'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': '${{ env.MSRV }}', 'profile': 'minimal'}}, 'jobs.check-msrv.steps[2]', {'name': 'install Rust ${{ matrix.toolchain }}', 'uses': 'dtolnay/rust-toolchain@master', 'with': {'toolchain': '${{ matrix.toolchain }}'}}), ('changed', 'jobs.check-msrv.steps[1].name', 'install Rust ${{ env.MSRV }}', 'jobs.check-msrv.steps[2].name', 'install Rust ${{ matrix.toolchain }}'), ('changed', 'jobs.check-msrv.steps[1].uses', 'actions-rs/toolchain@v1', 'jobs.check-msrv.steps[2].uses', 'dtolnay/rust-toolchain@master'), ('removed', 'jobs.check-msrv.steps[1].with.profile', 'minimal', None, None), ('changed', 'jobs.check-msrv.steps[1].with.toolchain', '${{ env.MSRV }}', 'jobs.check-msrv.steps[2].with.toolchain', '${{ matrix.toolchain }}'), ('removed', 'jobs.check-msrv.steps[3]', {'name': 'Select minimal versions', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'update', 'args': '-Z minimal-versions', 'toolchain': 'nightly'}}, None, None), ('removed', 'jobs.check-msrv.steps[4]', {'name': 'Check', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'check', 'args': '--workspace --all-features --locked --exclude=tracing-appender --exclude=tracing-examples --exclude=tracing-futures', 'toolchain': '${{ env.MSRV }}'}}, None, None), ('added', None, None, 'jobs.check-msrv.steps[3]', {'name': 'install cargo-hack', 'uses': 'taiki-e/install-action@cargo-hack'}), ('added', None, None, 'jobs.check-msrv.steps[4]', {'name': 'install cargo-minimal-versions', 'uses': 'taiki-e/install-action@cargo-minimal-versions'}), ('added', None, None, 'jobs.check-msrv.steps[5]', {'name': 'cargo minimal-versions check', 'working-directory': '${{ matrix.subcrate }}', 'run': 'CARGO_MINVER=(cargo minimal-versions check --feature-powerset --no-dev-deps)\ncase "${{ matrix.subcrate }}" in\n  tracing)\n    EXCLUDE_FEATURES=(\n      max_level_off max_level_error max_level_warn max_level_info\n      max_level_debug max_level_trace release_max_level_off\n      release_max_level_error release_max_level_warn\n      release_max_level_info release_max_level_debug\n      release_max_level_trace\n    )\n    ${CARGO_MINVER[@]} --exclude-features "${EXCLUDE_FEATURES[*]}"\n    ;;\n  tracing-subscriber)\n    INCLUDE_FEATURES=(fmt ansi json registry env-filter)\n    ${CARGO_MINVER[@]} --include-features "${INCLUDE_FEATURES[*]}"\n    ;;\n  tracing-futures)\n    EXCLUDE_FEATURES=(futures-01 futures_01 tokio tokio_01)\n    ${CARGO_MINVER[@]} --exclude-features "${EXCLUDE_FEATURES[*]}"\n    ;;\n  *)\n    ${CARGO_MINVER[@]}\n    ;;\nesac\n', 'shell': 'bash'}), ('removed', 'jobs.minimal-versions', {'name': 'cargo check (-Zminimal-versions)', 'needs': 'check', 'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v3'}, {'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'nightly', 'profile': 'minimal', 'override': True}}, {'name': 'install cargo-hack', 'uses': 'taiki-e/install-action@cargo-hack'}, {'name': 'check --all-features -Z minimal-versions', 'run': '# Remove dev-dependencies from Cargo.toml to prevent the next `cargo update`\n# from determining minimal versions based on dev-dependencies.\ncargo hack --remove-dev-deps --workspace\n# Update Cargo.lock to minimal version dependencies.\ncargo update -Z minimal-versions\ncargo hack check \\\n  --package tracing \\\n  --package tracing-core \\\n  --package tracing-subscriber \\\n  --all-features --ignore-private\n'}]}, None, None), ('removed', 'jobs.check-msrv-appender', {'name': 'cargo check (tracing-appender MSRV)', 'needs': 'check', 'runs-on': 'ubuntu-latest', 'steps': [{'uses': 'actions/checkout@v3'}, {'name': 'install Rust ${{ env.APPENDER_MSRV }}', 'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': '${{ env.APPENDER_MSRV }}', 'profile': 'minimal'}}, {'name': 'install Rust nightly', 'uses': 'actions-rs/toolchain@v1', 'with': {'toolchain': 'nightly', 'profile': 'minimal'}}, {'name': 'Select minimal versions', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'update', 'args': '-Z minimal-versions', 'toolchain': 'nightly'}}, {'name': 'Check', 'uses': 'actions-rs/cargo@v1', 'with': {'command': 'check', 'args': '--all-features --locked -p tracing-appender', 'toolchain': '${{ env.APPENDER_MSRV }}'}}]}, None, None)]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_32(self):       
        old_workflow = './test/test_cases/test32_old.yaml'
        new_workflow = './test/test_cases/test32_new.yaml'

        expected_result = [('removed', 'jobs.go118.steps[4]', {'run': 'go install github.com/google/go-containerregistry/cmd/registry@latest\nregistry &\nKO_DOCKER_REPO=localhost:1338 ko build ./test/\n'}, None, None), ('added', None, None, 'jobs.go118.steps[4]', {'uses': 'chainguard-dev/actions/setup-registry@main'}), ('added', None, None, 'jobs.go118.steps[5]', {'with': {'KO_DOCKER_REPO': 'localhost:1338'}, 'run': 'ko build ./test/'})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_33(self):       
        old_workflow = './test/test_cases/test33_old.yaml'
        new_workflow = './test/test_cases/test33_new.yaml'

        expected_result = [('added', None, None, 'jobs.build.strategy', {'matrix': {'channel': ['esphome', 'esphome-beta', 'esphome-dev']}}), ('changed', 'jobs.build.steps[1].name', '🚀 Run Home Assistant Add-on Lint on ESPHome', 'jobs.build.steps[1].name', '🚀 Run Home Assistant Add-on Lint on ${{ matrix.channel }}'), ('changed', 'jobs.build.steps[1].with.path', './esphome', 'jobs.build.steps[1].with.path', './${{ matrix.channel }}'), ('removed', 'jobs.build.steps[2]', {'name': '🚀 Run Home Assistant Add-on Lint on ESPHome-Beta', 'uses': 'frenck/action-addon-linter@v2', 'with': {'path': './esphome-beta'}}, None, None), ('removed', 'jobs.build.steps[3]', {'name': '🚀 Run Home Assistant Add-on Lint on ESPHome-Dev', 'uses': 'frenck/action-addon-linter@v2', 'with': {'path': './esphome-dev'}}, None, None)]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_34(self):       
        old_workflow = './test/test_cases/test34_old.yaml'
        new_workflow = './test/test_cases/test34_new.yaml'

        expected_result = [('removed', 'jobs.test.steps[9].with.fail_ci_if_error', True, None, None)]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_35(self):       
        old_workflow = './test/test_cases/test35_old.yaml'
        new_workflow = './test/test_cases/test35_new.yaml'

        expected_result = [('moved', 'jobs.test.steps[6]', {'name': 'Create app from template', 'env': {'TEMPLATE_NAME': '${{ matrix.template }}'}, 'run': 'ns create myApp --template="$(pwd)/templates/packages/$TEMPLATE_NAME"\ncd myApp\nnpm install\n'}, 'jobs.test.steps[7]', {'name': 'Create app from template', 'env': {'TEMPLATE_NAME': '${{ matrix.template }}'}, 'run': 'ns create myApp --template="$(pwd)/templates/packages/$TEMPLATE_NAME"\ncd myApp\nnpm install\n'}), ('moved', 'jobs.test.steps[7]', {'name': 'Test iOS Build', 'working-directory': 'myApp', 'run': 'ns build ios\n'}, 'jobs.test.steps[8]', {'name': 'Test iOS Build', 'working-directory': 'myApp', 'run': 'ns build ios\n'}), ('moved', 'jobs.test.steps[8]', {'name': 'Test Android Build', 'working-directory': 'myApp', 'run': 'ns build android\n'}, 'jobs.test.steps[9]', {'name': 'Test Android Build', 'working-directory': 'myApp', 'run': 'ns build android\n'}), ('added', None, None, 'jobs.test.steps[6]', {'name': 'Uninstall build-tools@31.0.0', 'run': 'SDKMANAGER=$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager\necho y | $SDKMANAGER --uninstall "build-tools;31.0.0"\n'})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_36(self):       
        old_workflow = './test/test_cases/test36_old.yaml'
        new_workflow = './test/test_cases/test36_new.yaml'

        expected_result = [('changed', 'jobs.build.strategy.matrix.os[1]', 'windows-lates', 'jobs.build.strategy.matrix.os[1]', 'windows-latest')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_37(self):       
        old_workflow = './test/test_cases/test37_old.yaml'
        new_workflow = './test/test_cases/test37_new.yaml'

        expected_result = [('changed', 'jobs.verify.steps[3].name', 'Check formattting', 'jobs.verify.steps[3].name', 'Check formatting')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_38(self):       
        old_workflow = './test/test_cases/test38_old.yaml'
        new_workflow = './test/test_cases/test38_new.yaml'

        expected_result = [('changed', 'jobs.build-and-test.steps[1].with.toolchain', 'nightly', 'jobs.build-and-test.steps[1].with.toolchain', 'nightly-2020-09-20')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_39(self):       
        old_workflow = './test/test_cases/test39_old.yaml'
        new_workflow = './test/test_cases/test39_new.yaml'

        expected_result = [('changed', 'jobs.build-switch.steps[0].run', 'wget "https://wii.leseratte10.de/devkitPro/devkitA64/r14 (2019-12)/devkitA64-r14-3-linux.pkg.tar.xz" && sudo dkp-pacman -U devkitA64-r14-3-linux.pkg.tar.xz --noconfirm', 'jobs.build-switch.steps[0].run', 'sudo dkp-pacman -Rs devkitA64 devkitA64-gdb devkita64-rules --noconfirm && wget "https://wii.leseratte10.de/devkitPro/devkitA64/r14 (2019-12)/devkitA64-r14-3-linux.pkg.tar.xz" && sudo dkp-pacman -U devkitA64-r14-3-linux.pkg.tar.xz --noconfirm')]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)

    def test_result_40(self):       
        old_workflow = './test/test_cases/test40_old.yaml'
        new_workflow = './test/test_cases/test40_new.yaml'

        expected_result = [('added', None, None, 'env', {'REGISTRY': 'ghcr.io', 'IMAGE_NAME': '${{ github.repository }}'}), ('moved', 'jobs.main.steps[6]', {'name': 'Image digest', 'run': 'echo ${{ steps.docker_build.outputs.digest }}'}, 'jobs.main.steps[7]', {'name': 'Image digest', 'run': 'echo ${{ steps.docker_build.outputs.digest }}'}), ('moved', 'jobs.main.steps[5]', {'name': 'Build', 'uses': 'docker/build-push-action@v3', 'with': {'file': './resources/Dockerfile', 'build-args': 'RUST_TOOLCHAIN=${{ env.toolchain }}\n', 'platforms': 'linux/arm64\nlinux/amd64\n', 'push': "${{ github.repository == 'cloud-hypervisor/rust-hypervisor-firmware' && github.event_name == 'push' }}", 'tags': 'rusthypervisorfirmware/dev:latest'}}, 'jobs.main.steps[6]', {'name': 'Build', 'uses': 'docker/build-push-action@v3', 'with': {'file': './resources/Dockerfile', 'build-args': 'RUST_TOOLCHAIN=${{ env.toolchain }}\n', 'platforms': 'linux/arm64\nlinux/amd64\n', 'push': "${{ github.event_name == 'push' }}", 'tags': '${{ steps.meta.outputs.tags }}'}}), ('changed', 'jobs.main.steps[5].with.push', "${{ github.repository == 'cloud-hypervisor/rust-hypervisor-firmware' && github.event_name == 'push' }}", 'jobs.main.steps[6].with.push', "${{ github.event_name == 'push' }}"), ('changed', 'jobs.main.steps[5].with.tags', 'rusthypervisorfirmware/dev:latest', 'jobs.main.steps[6].with.tags', '${{ steps.meta.outputs.tags }}'), ('removed', 'jobs.main.steps[4].if', "${{ github.repository == 'cloud-hypervisor/rust-hypervisor-firmware' && github.event_name == 'push' }}", None, None), ('changed', 'jobs.main.steps[4].name', 'Login to DockerHub', 'jobs.main.steps[4].name', 'Login to ghcr'), ('added', None, None, 'jobs.main.steps[4].with.registry', '${{ env.REGISTRY }}'), ('changed', 'jobs.main.steps[4].with.username', '${{ secrets.DOCKERHUB_USERNAME }}', 'jobs.main.steps[4].with.username', '${{ github.actor }}'), ('changed', 'jobs.main.steps[4].with.password', '${{ secrets.DOCKERHUB_TOKEN }}', 'jobs.main.steps[4].with.password', '${{ secrets.GITHUB_TOKEN }}'), ('added', None, None, 'jobs.main.steps[5]', {'name': 'Extract metadata (tags, labels) for Docker', 'id': 'meta', 'uses': 'docker/metadata-action@v4', 'with': {'images': '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}', 'flavor': 'latest=true\n'}})]

        assert compare_results(gawd.diff_workflow_files(old_workflow, new_workflow), expected_result)