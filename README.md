# Song Search Player

A one-page tool for auditioning a long list of early-2000s Christian songs by their first few seconds. It is live at https://brycewalls.github.io/song-search/.

Each song plays from the first second through YouTube. Mark it "Not it," "Maybe," or "This is it," and the next one starts.

- `index.html` is the whole page.
- `songs.json` is the song list (title, artist, album, year, YouTube ID, and Spotify ID where known). Sections: S solo artists, W WOW Hits, G groups, X more Christian artists, M mainstream pop and rock.
- `progress.json` is the starting set of marks. On the live site, new marks save in your browser.
- `server.py` is an optional local server (`python3 server.py 8797`) that saves marks to `progress.json` instead.

Keys: N or right arrow for "Not it," M for maybe, Y for "This is it," B to go back, R to replay, S to skip, and U to clear a mark.

This README is also the guide to how work on this project is tracked.

- Issues (bugs, changes, roadmap): https://github.com/brycewalls/song-search/issues
- CI runs and page screenshots: https://github.com/brycewalls/song-search/actions
- Releases: https://github.com/brycewalls/song-search/releases

## The loop

1. **It starts as an issue.** A bug, a change, a roadmap idea.
2. **Work happens on a branch named for the issue:** `fix/12-short-name`, `feat/20-short-name`.
3. **A pull request brings it back to `main`** with `Closes #12` in the body. CI opens the page at desktop and phone widths on the PR.
4. **Merging to `main` is the build and the deploy.** GitHub Pages serves `main`.
5. **A tag makes a release** when a version is worth marking.

## Testing

- **CI on every push:** the page at two widths, zero console errors, no failed requests, no overflow.
- **By hand:** press Start and confirm a song plays inside the page. CI can't check YouTube playback.
