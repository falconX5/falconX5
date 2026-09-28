# Install your Bitcrest GitHub profile

This package is a GitHub profile README with two self-contained looping GIF animations.

1. Sign in to the personal GitHub account whose username is **Bitcrest**.
2. Create a **public** repository named **Bitcrest**, or open the existing one.
3. Extract this ZIP on your computer.
4. Upload **README.md** and the entire **assets** folder to the repository root. On GitHub, use **Add file → Upload files**, then commit the upload. If a README already exists, replace its content with this package's README.
5. Open https://github.com/Bitcrest to see the profile.

The repository should contain `README.md`, `assets/bitcrest-banner.gif`, and `assets/workbench.gif`. Upload the contents of the extracted folder, not the outer `Bitcrest-profile` folder. Uploading the ZIP itself will not install the profile.

GitHub requires a public repository matching the account's actual username, with a nonempty README.md in the root. If Bitcrest is your display name but your username is different, use your actual username for the repository and replace the GitHub link in README.md. If Bitcrest is an organization, use a public `.github` repository with the README at `profile/README.md` and place `assets` next to that README instead.

## Customize

- **Project descriptions:** edit the “What I'm building” table in README.md.
- **Project links:** add your actual repository URLs when ready. Project repository names were not supplied, so none were guessed.
- **Introduction and skills:** edit the corresponding sections in README.md.
- **Animations:** edit `tools/generate_assets.py` and regenerate them with Python and Pillow. The source looks for DejaVu fonts on Linux and falls back to Arial/Consolas on Windows. Set `BITCREST_FONT_DIR` to a folder with DejaVuSans.ttf, DejaVuSans-Bold.ttf, and DejaVuSansMono.ttf to use custom font locations.
- **Static option:** replace `.gif` with `.png` in the two README image paths to use the included still images.

To regenerate assets from the extracted project directory:

```sh
python -m pip install Pillow
python tools/generate_assets.py
```

No API keys, GitHub Actions, external image services, or deployment are needed. All animation is embedded in repository assets. The workbench is a designed introduction, not live telemetry or a screenshot of project results.

This package has been created for upload; it has not been published to your GitHub account.

GitHub setup reference: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

Organization setup reference: https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile
