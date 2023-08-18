# TS PNG Release Procedure

Procedure for releasing a new TS PNG package on GitHub and on PyPi.

## GitHub Release

1. Add changes made since the previous release to `CHANGELOG.md` by referring to the closed pull requests. The header should have 'IN PROGRESS' in the date section.

2. Commit this change with the message 'Add changes to documentation'.

3. Change the date in `CHANGELOG.md` to the current date in the format YYYY-MM-DD.

4. Commit this change with the message 'Add release date'.

5. Change the package version in both `pyproject.toml` and `setup.py`.

6. Commit these changes with the message 'Bump package version'.

7. Publish the branch and create the pull request.

8. When the PR is approved, merge the branch and locally pull the updated repository.

   ```sh
   git checkout main && git pull
   ```

9. Create the release tag.

   ```sh
   git tag -a v#.#.# -m "#.#.# (YYYY-MM-DD)"
   ```

10. Push the tags.

   ```sh
   git push --tags
   ```

11. Go to the draft of the release on Github and publish it.

12. Create the next milestone, move open issues to the next milestone, and close the previous milestone.

## PyPi Release

1. Pull the latest changes from the repository.

   ```sh
   git checkout main && git pull
   ```

2. Activate the virtual environment.

   ```sh
   source .venv/bin/activate
   ```

3. Remove all files in the `dist` folder.

4. Build the wheel.

   ```sh
   python3 -m build ./
   ```

5. Upload the build and enter PyPi credentials when prompted.

   ```sh
   twine upload dist/*
   ```
