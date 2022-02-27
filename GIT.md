# **GIT**
## SPIS TREŚCI
* [DEFINICJE](#DEFINICJE)
* [KOMENDY](#KOMENDY)
	* [git config](#git-config)
	* [git init](#git-init)
	* [git remote](#git-remote)
	* [git clone](#git-clone)
	* [git pull](#git-pull)
	* [git status](#git-status)
	* [git push](#git-push)

##  DEFINICJE
`GIT` - rozproszony system kontroli wersji
`remote` - centralne repozytorium
`local` - lokalne repozytorium
branch
commit
stage

##   KOMENDY
### git config
```bash
git config --global user.name "<username>"
git config --global user.email "<email>"
```
### git init
```bash
git init
```
 ### git remote
```bash
git remote add origin "<remote_repository_url>"
```
### git clone
Klonowanie repozytorium z podanego linka
```bash
git clone "<remote_repository_url>"
```
### git pull
Aktualizowanie lokalnego repozytorium o nowe commity z repozytorium centralnego z aktualnego brancha 
```bash
git pull
```
### git status
```bash
git status
```

### git push
Wypychanie zmian na aktualnym branchu z lokalnego repozytorium do repozytorium centralnego 
```bash
git push
```