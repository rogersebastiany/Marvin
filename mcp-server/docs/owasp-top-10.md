if(Cookies.get('cookies-ok') == 'true' && window.ga === undefined)
{
window.ga=window.ga||function(){(ga.q=ga.q||[]).push(arguments)};ga.l=+new Date;
ga('create', 'UA-4531126-1', 'auto');
ga('send', 'pageview');
}
else if (Cookies.get('cookies-ok') == 'true')
{
ga('send', 'pageview');
}
function handleOutboundLinkClicks(event) {
var href = '';
if(event.target.href == undefined)
href = event.target.parentElement.href;
else
href = event.target.href
if(Cookies.get('cookies-ok') == 'true'){
ga('send', 'event', {
eventCategory: 'Outbound Link',
eventAction: 'click',
eventLabel: href,
transport: 'beacon'
});
}
}

OWASP Top Ten Web Application Security Risks | OWASP Foundation

$(function(){
var baseurl = "https://github.com/OWASP/www-project-top-ten/blob/master/";
var path = "index.md";
$('.repo').html('<a href=' + baseurl + path + '><div class="reset-3c756112--menuItemIcon-206eb252" style="float: left;"><svg preserveAspectRatio="xMidYMid meet" height="1em" width="1em" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 438.549 438.549" stroke="none" class="icon-7f6730be--text-3f89f380"><g><path d="M409.132 114.573c-19.608-33.596-46.205-60.194-79.798-79.8-33.598-19.607-70.277-29.408-110.063-29.408-39.781 0-76.472 9.804-110.063 29.408-33.596 19.605-60.192 46.204-79.8 79.8C9.803 148.168 0 184.854 0 224.63c0 47.78 13.94 90.745 41.827 128.906 27.884 38.164 63.906 64.572 108.063 79.227 5.14.954 8.945.283 11.419-1.996 2.475-2.282 3.711-5.14 3.711-8.562 0-.571-.049-5.708-.144-15.417a2549.81 2549.81 0 0 1-.144-25.406l-6.567 1.136c-4.187.767-9.469 1.092-15.846 1-6.374-.089-12.991-.757-19.842-1.999-6.854-1.231-13.229-4.086-19.13-8.559-5.898-4.473-10.085-10.328-12.56-17.556l-2.855-6.57c-1.903-4.374-4.899-9.233-8.992-14.559-4.093-5.331-8.232-8.945-12.419-10.848l-1.999-1.431c-1.332-.951-2.568-2.098-3.711-3.429-1.142-1.331-1.997-2.663-2.568-3.997-.572-1.335-.098-2.43 1.427-3.289 1.525-.859 4.281-1.276 8.28-1.276l5.708.853c3.807.763 8.516 3.042 14.133 6.851 5.614 3.806 10.229 8.754 13.846 14.842 4.38 7.806 9.657 13.754 15.846 17.847 6.184 4.093 12.419 6.136 18.699 6.136 6.28 0 11.704-.476 16.274-1.423 4.565-.952 8.848-2.383 12.847-4.285 1.713-12.758 6.377-22.559 13.988-29.41-10.848-1.14-20.601-2.857-29.264-5.14-8.658-2.286-17.605-5.996-26.835-11.14-9.235-5.137-16.896-11.516-22.985-19.126-6.09-7.614-11.088-17.61-14.987-29.979-3.901-12.374-5.852-26.648-5.852-42.826 0-23.035 7.52-42.637 22.557-58.817-7.044-17.318-6.379-36.732 1.997-58.24 5.52-1.715 13.706-.428 24.554 3.853 10.85 4.283 18.794 7.952 23.84 10.994 5.046 3.041 9.089 5.618 12.135 7.708 17.705-4.947 35.976-7.421 54.818-7.421s37.117 2.474 54.823 7.421l10.849-6.849c7.419-4.57 16.18-8.758 26.262-12.565 10.088-3.805 17.802-4.853 23.134-3.138 8.562 21.509 9.325 40.922 2.279 58.24 15.036 16.18 22.559 35.787 22.559 58.817 0 16.178-1.958 30.497-5.853 42.966-3.9 12.471-8.941 22.457-15.125 29.979-6.191 7.521-13.901 13.85-23.131 18.986-9.232 5.14-18.182 8.85-26.84 11.136-8.662 2.286-18.415 4.004-29.263 5.146 9.894 8.562 14.842 22.077 14.842 40.539v60.237c0 3.422 1.19 6.279 3.572 8.562 2.379 2.279 6.136 2.95 11.276 1.995 44.163-14.653 80.185-41.062 108.068-79.226 27.88-38.161 41.825-81.126 41.825-128.906-.01-39.771-9.818-76.454-29.414-110.049z"></path></g></svg><span style="padding-left:8px;">Edit on GitHub</span></div></a>');
});

For full functionality of this site it is necessary to enable JavaScript. Here are the  [instructions how to enable JavaScript in your web browser](http://turnonjs.com/).

#banner img {
max-width: 30em;
}
@media (max-width: 1131px) {
#banner img {
max-width: 30em;
}
}
@media (max-width: 800px) {
#banner img {
max-width: 20em;
}
}
@media (max-width: 600px) {
#banner img {
max-width: 20em;
}
}
@media (max-width: 450px) {
#banner img {
max-width: 250px;
}
}

$(function () {
var bannerdata = [];
banneryaml = YAML.load('https://owasp.org/www-project-top-ten/assets/sitedata/banner-data.yml');
$.each(banneryaml, function (index) {
bannerdata.push(this);
});
if (bannerdata.length > 0) {
var htmlstring = "";
var usebanner = null;
var defbanner = null;
var checkdate = new Date(); //local time but who cares about the time?
bannerdata.forEach(data => {
if (data.start) {
var start = data.start;
if (data.start <= checkdate) {
if (data.end) {
var end = data.end;
if (checkdate < end) {
usebanner = data;
}
}
else
usebanner = data;
}
}
else {
defbanner = data;
}
});
if (defbanner && !usebanner)
usebanner = defbanner;
if (usebanner) {
htmlstring = usebanner.text;
htmlstring += "<a href='#' id='close-banner' aria-label='close announcement' style='float:right;'><i class='fa fa-times'></i></a>";
$("#banner").html(htmlstring);
$("#banner").removeClass("notice");
$("#banner").addClass(usebanner.type);
$("#close-banner").click(function() {
$(this).closest("#banner").remove();
Cookies.set('banner-seen', 'true', { expires: 7 });
});
}
}
});
#banner img {
max-width: 30em;
}
@media (max-width: 1131px) {
#banner img {
max-width: 30em;
}
}
@media (max-width: 800px) {
#banner img {
max-width: 20em;
}
#popup {
visibility: hidden;
}
}
@media (max-width: 600px) {
#popup {
visibility: hidden;
}
#banner img {
max-width: 20em;
}
}
@media (max-width: 450px) {
#banner img {
max-width: 250px;
}
#popup {
visibility: hidden;
}
}

$(function () {
var popdata = [];
$("#popup").hide();
popyaml = YAML.load('https://owasp.org/www-project-top-ten/assets/sitedata/popup-data.yml');
$.each(popyaml, function (index) {
popdata.push(this);
});
if (popdata.length > 0) {
var htmlstring = "";
var usepop = null;
var defpop = null;
var checkdate = new Date(); //local time but who cares about the time?
popdata.forEach(data => {
if (data.start) {
var start = data.start;
if (data.start <= checkdate) {
if (data.end) {
var end = data.end;
if (checkdate < end) {
usepop = data;
}
}
else
usepop = data;
}
}
else {
defpop = data;
}
});
if (defpop && !usepop)
usepop = defpop;
if (usepop) {
htmlstring = usepop.text;
htmlstring += "<a href='#' id='close-popup' aria-label='close announcement' style='float:right;'><i class='fa fa-times'></i></a>";
$("#popup").html(htmlstring);
$("#popup").removeClass("notice");
$("#popup").addClass(usepop.type);
if( Cookies.get('popup-seen')!='true')
{
$("#popup").show();
}
$("#close-popup").click(function() {
$(this).closest("#popup").remove();
Cookies.set('popup-seen', 'true', { expires: 7 });
});
}
}
});

[Store](https://owasp.org/store)
[Donate](https://owasp.org/donate?reponame=www-project-top-ten&title=OWASP+Top+Ten+Web+Application+Security+Risks)
[Join](https://owasp.glueup.com/organization/6727/memberships)

This website uses cookies to analyze our traffic and only share that information with our analytics partners.

Accept

x

[Store](https://owasp.org/store)

[Donate](https://owasp.org/donate?reponame=www-project-top-ten&title=OWASP+Top+Ten+Web+Application+Security+Risks)

[Join](https://owasp.glueup.com/organization/6727/memberships)

$(function(){
url = $(location).attr('href');
if(url.includes('www2'))
{
url = url.replace(/www2./, '');
$(location).attr('href',url);
return;
}
// this works to get data from a json file NOT in data
$.getJSON("https://owasp.org/www--site-theme/assets/sitedata/menus.json", function(data) {
var listr = "<ul aria-label='header menu'>";
var mlistr = "<ul class='mobile-menu hide-el' role='navigation' aria-label='mobile primary navigation'>";
mlistr += "<li><a href='#' class='menu-toggler' aria-hidden='true'><i class='fa fa-times'></i></a></li>";
mlistr += "<li>";
mlistr += "<form role='search' method='get' action='https://owasp.org/search'>";
mlistr += "<div class='search-div'>";
mlistr += "<input id='searchString' aria-label='search input' name='searchString' class='search-bar' type='search' placeholder='Search OWASP.org' required='true'>";
mlistr += "<button id='search-button' aria-label='search button' type='submit' class='fa fa-search' style='padding-left: 8px;'></button></div></form>";
mlistr += "</li>";
$.each(data.menus, function (ndx, menu){
listr += "<li><a href='" + menu.url + "'>" + menu.title + "</a>";
searchitem = issearch(menu.title);
if(!menu.items && !searchitem)
{
mlistr += "<li><a href='" + menu.url + "'>" + menu.title + "</a>";
}
if(menu.items){
listr += "<ul class='dropdown-menu'>";
if(!searchitem) {
mlistr += "<button class='accordion'>" + menu.title + "</button>";
mlistr += "<div class='panel'>";
mlistr += "<ul>";
}
$.each(menu.items, function(ndx, item){
if(item.separator)
{
listr += "<li class='separator'>";
if(!searchitem)
mlistr += "<li class='separator'>";
}
else
{
listr += "<li>";
if(!searchitem)
mlistr += "<li>";
}
listr += "<a href='" + item.url + "'";
if(!searchitem)
mlistr += "<a href='" + item.url + "'";
if(item.opentab)
{
listr += " target='\_blank' rel='noopener noreferrer'";
if(!searchitem)
mlistr += " target='\_blank' rel='noopener noreferrer'";
}
listr += ">" + item.title + "</a></li>";
if(!searchitem)
mlistr += ">" + item.title + "</a></li>";
});
listr += "</ul>";
if(!searchitem){
mlistr += "</ul>";
mlistr += "</div>";
}
}
listr += "</li>";
if(!searchitem)
mlistr += "</li>";
});
listr += "</ul>";
mlistr += "<li><a href='https://owasp.org/donate'>MAKE A DONATION</a></li>";
mlistr += "<li><a href='https://owasp.org/membership'>BECOME A MEMBER</a></li>";
mlistr += "<li><a href='https://owasp.org/sitemap'>SITEMAP</a></li>";
mlistr += "</ul>";
//$('.desktop-logo').after(listr);
$('#midmenu').html(listr);
$('#overlay').after(mlistr);
$(".accordion").click(function () {
$(this).toggleClass("active");
if($(this).next('.panel').css('display') == 'block'){
$(this).next('.panel').css('display', 'none');
}
else {
$(this).next('.panel').css('display', 'block');
}
});
$(".menu-toggler").click(function() {
$(".mobile-menu").toggleClass('hide-el');
});
});
});
function issearch(title) {
return title.indexOf('fa fa-search') > -1;
}

* [Main](#div-main)
* [Translation Efforts](#div-translation_efforts)
* [Sponsors](#div-sponsors)
* [Data 2025](#div-data_2025)

$(function() {
if(window.location.href.indexOf('#') != -1)
{
divid = window.location.href.substring(window.location.href.indexOf('#'))
secid = divid;
if(divid.indexOf('div-') >= 0)
{
$('.tab-link').each(function () {
divid = '#sec-' + $(this).attr('id').toLowerCase().replace('-link', '');
$(divid).addClass('tab-hidden');
$(this).removeClass('current');
});
secid = secid.replace('div-', 'sec-');
$(secid).removeClass('tab-hidden');
linkid = "#" + secid.substring(secid.indexOf('-') + 1) + "-link";
$(linkid).addClass('current');
}
}
});
$('.tab-link').click(function (e) {
e.preventDefault();
$('.tab-link').each(function () {
$(this).removeClass('current');
divid = '#sec-' + $(this).attr('id').toLowerCase().replace('-link', '');
$(divid).addClass('tab-hidden');
});
divid = '#sec-' + $(this).attr('id').toLowerCase().replace('-link', '');
$(this).addClass('current');
$(divid).removeClass('tab-hidden');
return false;
});

# OWASP Top Ten Web Application Security Risks

The most current released version is the [OWASP Top Ten 2025](https://owasp.org/Top10/2025/).

Previous versions are available at [OWASP Top Ten 2021](https://owasp.org/Top10/2021/) and [OWASP Top 10 2017 (PDF)](/www-pdf-archive/OWASP_Top_10-2017_%28en%29.pdf.pdf). Older versiona are available in the [Github repo](https://github.com/OWASP/Top10).

The OWASP Top 10 is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications.

Globally recognized by developers as the first step towards more secure coding.

Companies should adopt this document and start the process of ensuring that their web applications minimize these risks. Using the OWASP Top 10 is perhaps the most effective first step towards changing the software development culture within your organization into one that produces more secure code.

---

# Translation Efforts

Efforts have been made in numerous languages to translate the OWASP Top 10 - 2025. If you are interested in helping, please contact the members of the team for the language you are interested in contributing to, or if you don’t see your language listed (neither here nor at [github](https://github.com/OWASP/Top10/issues?utf8=%E2%9C%93&q=is%3Aissue)), please email [[email protected]](/cdn-cgi/l/email-protection) to let us know that you want to help and we’ll form a volunteer group for your language.

### Top10:2025 Completed Translations:

*Translations in progress - check back soon!*

## Historic:

### Top10:2021 Completed Translations:

* [**ar - العربية**](https://owasp.org/Top10/ar/)
* [**es - Español**](https://owasp.org/Top10/es/)
* [**fr - Français**](https://owasp.org/Top10/fr/)
* [**id - Indonesian**](https://owasp.org/Top10/id/)
* [**it - Italiano**](https://owasp.org/Top10/it/)
* [**ja - 日本語]**](https://owasp.org/Top10/ja/)
* [**pt\_BR - Português (Brasil)**](https://owasp.org/Top10/pt_BR/)
* [**zh\_CN - 简体中文**](https://owasp.org/Top10/zh_CN/)
* [**zh\_TW - 繁體中文**](https://owasp.org/Top10/zh_TW/)

### Top10:2017 Completed Translations:

* **Chinese:** [OWASP Top 10-2017 - 中文版（PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10_2017_%E4%B8%AD%E6%96%87%E7%89%88v1.3.pdf)  
  + 项目组长：[王颉](https://wiki.owasp.org/index.php/User:Jie_Wang)（[[email protected]](/cdn-cgi/l/email-protection)）
  + 翻译人员：陈亮、王厚奎、王颉、王文君、王晓飞、吴楠、徐瑞祝、夏天泽、杨璐、张剑钟、赵学文（排名不分先后，按姓氏拼音排列）
  + 审查人员：Rip、包悦忠、李旭勤、杨天识、张家银（排名不分先后，按姓氏拼音排列）
  + 汇编人员：赵学文
* **French:** [OWASP Top 10 2017 in French (Git/Markdown)](https://github.com/OWASP/Top10/tree/master/2017/fr)
* **German:** [OWASP Top 10 2017 in German V1.0 (Pdf)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10-2017_de_V1.0.pdf) [(web pages)](2017/de/)  
  compiled by Christian Dresen, Alexios Fakos, Louisa Frick, Torsten Gigler, Tobias Glemser, Dr. Frank Gut, Dr. Ingo Hanke, Dr. Thomas Herzog, Dr. Markus Koegel, Sebastian Klipper, Jens Liebau, Ralf Reinhardt, Martin Riedel, Michael Schaefer
* **Hebrew:** [OWASP Top 10-2017 - Hebrew (PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP-Top-10-2017-he.pdf)  [(PPTX)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP-Top-10-2017-he.pptx)  
  translated by Eyal Estrin (Twitter: @eyalestrin) and Omer Levi Hevroni (Twitter: @omerlh).
* **Japanese:** [OWASP Top 10-2017 - 日本語版 (PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10-2017%28ja%29.pdf)  
   translated and reviewed by Akitsugu ITO, Albert Hsieh, Chie TAZAWA, Hideko IGARASHI, Hiroshi TOKUMARU, Naoto KATSUMI, Riotaro OKADA, Robert DRACEA, Satoru TAKAHASHI, Sen UENO, Shoichi NAKATA, Takanori NAKANOWATARI ,Takanori ANDO, Tomohiro SANAE.
* **Korean:** [OWASP Top 10-2017 - 한글 (PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10-2017-ko.pdf)  [(PPTX)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10-2017-ko.pptx)  
   번역 프로젝트 관리 및 감수 : 박형근(Hyungkeun Park) / 감수(ㄱㄴㄷ순) : 강용석(YongSeok Kang), 박창렴(Park Changryum), 조민재(Johnny Cho) / 편집 및 감수 : 신상원(Shin Sangwon) / 번역(ㄱㄴㄷ순) : 김영하(Youngha Kim), 박상영(Sangyoung Park), 이민욱(MinWook Lee), 정초아(JUNG CHOAH), 조광렬(CHO KWANG YULL), 최한동(Handong Choi)
* **Portuguese:** [OWASP Top 10 2017 - Portuguese (PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10-2017-pt_pt.pdf) [(ODP)](https://github.com/OWASP/Top10/raw/master/2017/OWASP%20Top%2010-2017-pt_pt.odp)  
   translated by Anabela Nogueira, Carlos Serrão, Guillaume Lopes, João Pinto, João Samouco, Kembolle A. Oliveira, Paulo A. Silva, Ricardo Mourato, Rui Silva, Sérgio Domingues, Tiago Reis, Vítor Magano.
* **Russian:** [OWASP Top 10-2017 - на русском языке (PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP Top 10-2017-ru.pdf)  
   translated and reviewed by JZDLin ([@JZDLin](https://github.com/JZDLin)), Oleksii Skachkov ([@hamster4n](https://github.com/hamster4n)), Ivan Kochurkin ([@KvanTTT](https://github.com/KvanTTT)) and [Taras Ivashchenko](https://wiki.owasp.org/index.php/User:Taras_Ivashchenko)
* **Spanish:** [OWASP Top 10-2017 - Español (PDF)](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP-Top-10-2017-es.pdf)  
  + [Gerardo Canedo](https://wiki.owasp.org/index.php/User:Gerardo_Canedo)（[[email protected]](/cdn-cgi/l/email-protection) - [Twitter: @GerardoMCanedo])
  + [Cristian Borghello](https://wiki.owasp.org/index.php/User:Cristian_Borghello)（[[email protected]](/cdn-cgi/l/email-protection) - [Twitter: @seguinfo])

### Top10:2017 Release Candidate Translation Teams:

* Azerbaijanian: Rashad Aliyev ([[email protected]](/cdn-cgi/l/email-protection))
* Chinese RC2:Rip、包悦忠、李旭勤、王颉、王厚奎、吴楠、徐瑞祝、夏天泽、张家银、张剑钟、赵学文(排名不分先后，按姓氏拼音排列) [OWASP Top10 2017 RC2 - Chinese PDF](https://www.owasp.org/images/d/d6/OWASP_Top_10_2017%EF%BC%88RC2%EF%BC%89%E4%B8%AD%E6%96%87%E7%89%88%EF%BC%88%E5%8F%91%E5%B8%83%E7%89%88%EF%BC%89.pdf)
* French: Ludovic Petit: [[email protected]](/cdn-cgi/l/email-protection), Sébastien Gioria: [[email protected]](/cdn-cgi/l/email-protection).
* Others to be listed.

### Top10:2013 Completed Translations:

* Arabic: [OWASP Top 10 2013 - Arabic PDF](https://www.owasp.org/images/6/6a/OWASP_TOP_10_2013_Arabic.pdf)  
  Translated by: Mohannad Shahat: [[email protected]](/cdn-cgi/l/email-protection), Fahad: @SecurityArk, Abdulellah Alsaheel: [[email protected]](/cdn-cgi/l/email-protection), Khalifa Alshamsi: [[email protected]](/cdn-cgi/l/email-protection) and Sabri(KING SABRI): [[email protected]](/cdn-cgi/l/email-protection), Mohammed Aldossary: [[email protected]](/cdn-cgi/l/email-protection)
* Chinese 2013：中文版2013 [OWASP Top 10 2013 - Chinese (PDF)](https://www.owasp.org/images/5/51/OWASP_Top_10_2013-Chinese-V1.2.pdf).  
  项目组长： Rip、王颉， 参与人员： 陈亮、 顾庆林、 胡晓斌、 李建蒙、 王文君、 杨天识、 张在峰
* Czech 2013: [OWASP Top 10 2013 - Czech (PDF)](https://www.owasp.org/images/f/f3/OWASP_Top_10_-_2013_Final_-_Czech_V1.1.pdf) [OWASP Top 10 2013 - Czech (PPTX)](https://www.owasp.org/images/0/02/OWASP_Top_10_-_2013_Final_-_Czech_V1.1.pptx)  
  CSIRT.CZ - CZ.NIC, z.s.p.o. (.cz domain registry): Petr Zavodsky: [[email protected]](/cdn-cgi/l/email-protection), Vaclav Klimes, Zuzana Duracinska, Michal Prokop, Edvard Rejthar, Pavel Basta
* French 2013: [OWASP Top 10 2013 - French PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP%20Top%2010%20-%202013%20-%20French.pdf)  
  Ludovic Petit: [[email protected]](/cdn-cgi/l/email-protection), Sébastien Gioria: [[email protected]](/cdn-cgi/l/email-protection), Erwan Abgrall: [[email protected]](/cdn-cgi/l/email-protection), Benjamin Avet: [[email protected]](/cdn-cgi/l/email-protection), Jocelyn Aubert: [[email protected]](/cdn-cgi/l/email-protection), Damien Azambour: [[email protected]](/cdn-cgi/l/email-protection), Aline Barthelemy: [[email protected]](/cdn-cgi/l/email-protection), Moulay Abdsamad Belghiti: [[email protected]](/cdn-cgi/l/email-protection), Gregory Blanc: [[email protected]](/cdn-cgi/l/email-protection), Clément Capel: [[email protected]](/cdn-cgi/l/email-protection), Etienne Capgras: [[email protected]](/cdn-cgi/l/email-protection), Julien Cayssol: [[email protected]](/cdn-cgi/l/email-protection), Antonio Fontes: [[email protected]](/cdn-cgi/l/email-protection), Ely de Travieso: [[email protected]](/cdn-cgi/l/email-protection), Nicolas Grégoire: [[email protected]](/cdn-cgi/l/email-protection), Valérie Lasserre: [[email protected]](/cdn-cgi/l/email-protection), Antoine Laureau: [[email protected]](/cdn-cgi/l/email-protection), Guillaume Lopes: [[email protected]](/cdn-cgi/l/email-protection), Gilles Morain: [[email protected]](/cdn-cgi/l/email-protection), Christophe Pekar: [[email protected]](/cdn-cgi/l/email-protection), Olivier Perret: [[email protected]](/cdn-cgi/l/email-protection), Michel Prunet: [[email protected]](/cdn-cgi/l/email-protection), Olivier Revollat: [[email protected]](/cdn-cgi/l/email-protection), Aymeric Tabourin: [[email protected]](/cdn-cgi/l/email-protection)
* German 2013: [OWASP Top 10 2013 - German PDF](https://wiki.owasp.org/?title=Special:Redirect/file/OWASP_Top_10_2013_DE_Version_1_0.pdf)  
  [[email protected]](/cdn-cgi/l/email-protection) which is Frank Dölitzscher, Torsten Gigler, Tobias Glemser, Dr. Ingo Hanke, Thomas Herzog, [Kai Jendrian](https://wiki.owasp.org/index.php/User:Kai_Jendrian), [Ralf Reinhardt](https://wiki.owasp.org/index.php/User:Ralf_Reinhardt), Michael Schäfer
* Hebrew 2013: [OWASP Top 10 2013 - Hebrew](https://wiki.owasp.org/index.php/OWASP_Top10_Hebrew) [PDF](https://www.owasp.org/images/1/1b/OWASP_Top_10_2013-Hebrew.pdf)  
  Translated by: Or Katz, Eyal Estrin, Oran Yitzhak, Dan Peled, Shay Sivan.
* Italian 2013: [OWASP Top 10 2013 - Italian PDF](https://www.owasp.org/images/c/c9/OWASP_Top_10_-_2013_-_Italiano.pdf)  
  Translated by: Michele Saporito: [[email protected]](/cdn-cgi/l/email-protection), Paolo Perego: [[email protected]](/cdn-cgi/l/email-protection), Matteo Meucci: [[email protected]](/cdn-cgi/l/email-protection), Sara Gallo: [[email protected]](/cdn-cgi/l/email-protection), Alessandro Guido: [[email protected]](/cdn-cgi/l/email-protection), Mirko Guido Spezie: [[email protected]](/cdn-cgi/l/email-protection), Giuseppe Di Cesare: [[email protected]](/cdn-cgi/l/email-protection), Paco Schiaffella: [[email protected]](/cdn-cgi/l/email-protection), Gianluca Grasso: [[email protected]](/cdn-cgi/l/email-protection), Alessio D’Ospina: [[email protected]](/cdn-cgi/l/email-protection), Loredana Mancini: [[email protected]](/cdn-cgi/l/email-protection), Alessio Petracca: [[email protected]](/cdn-cgi/l/email-protection), Giuseppe Trotta: [[email protected]](/cdn-cgi/l/email-protection), Simone Onofri: [[email protected]](/cdn-cgi/l/email-protection), Francesco Cossu: [[email protected]](/cdn-cgi/l/email-protection), Marco Lancini: [[email protected]](/cdn-cgi/l/email-protection), Stefano Zanero: [[email protected]](/cdn-cgi/l/email-protection), Giovanni Schmid: [[email protected]](/cdn-cgi/l/email-protection), Igor Falcomata’: [[email protected]](/cdn-cgi/l/email-protection)
* Japanese 2013: [OWASP Top 10 2013 - Japanese PDF](https://www.owasp.org/images/7/79/OWASP_Top_10_2013_JPN.pdf)  
  Translated by: Chia-Lung Hsieh: ryusuke.tw(at)gmail.com, Reviewed by: Hiroshi Tokumaru, Takanori Nakanowatari
* Korean 2013: [OWASP Top 10 2013 - Korean PDF](https://www.owasp.org/images/2/2c/OWASP_Top_10_-_2013_Final_-_Korean.pdf) (이름가나다순)  
  김병효:[[email protected]](/cdn-cgi/l/email-protection), 김지원:[[email protected]](/cdn-cgi/l/email-protection), 김효근:[[email protected]](/cdn-cgi/l/email-protection), 박정훈:[[email protected]](/cdn-cgi/l/email-protection), 성영모:[[email protected]](/cdn-cgi/l/email-protection), 성윤기:[[email protected]](/cdn-cgi/l/email-protection), 송보영:[[email protected]](/cdn-cgi/l/email-protection), 송창기:[[email protected]](/cdn-cgi/l/email-protection), 유정호:[[email protected]](/cdn-cgi/l/email-protection), 장상민:[[email protected]](/cdn-cgi/l/email-protection), 전영재:[[email protected]](/cdn-cgi/l/email-protection), 정가람:[[email protected]](/cdn-cgi/l/email-protection), 정홍순:[[email protected]](/cdn-cgi/l/email-protection), 조민재:[[email protected]](/cdn-cgi/l/email-protection),허성무:[[email protected]](/cdn-cgi/l/email-protection)
* Brazilian Portuguese 2013: [OWASP Top 10 2013 - Brazilian Portuguese PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP_Top_10_-_2013_Brazilian_Portuguese.pdf)  
  Translated by: Carlos Serrão, Marcio Machry, Ícaro Evangelista de Torres, Carlo Marcelo Revoredo da Silva, Luiz Vieira, Suely Ramalho de Mello, Jorge Olímpia, Daniel Quintão, Mauro Risonho de Paula Assumpção, Marcelo Lopes, Caio Dias, Rodrigo Gularte
* Spanish 2013: [OWASP Top 10 2013 - Spanish PDF](https://www.owasp.org/images/5/5f/OWASP_Top_10_-_2013_Final_-_Espa%C3%B1ol.pdf)  
  Gerardo Canedo: [[email protected]](/cdn-cgi/l/email-protection), Jorge Correa: [[email protected]](/cdn-cgi/l/email-protection), Fabien Spychiger: [[email protected]](/cdn-cgi/l/email-protection), Alberto Hill: [[email protected]](/cdn-cgi/l/email-protection), Johnatan Stanley: [[email protected]](/cdn-cgi/l/email-protection), Maximiliano Alonzo: [[email protected]](/cdn-cgi/l/email-protection), Mateo Martinez: [[email protected]](/cdn-cgi/l/email-protection), David Montero: [[email protected]](/cdn-cgi/l/email-protection), Rodrigo Martinez: [[email protected]](/cdn-cgi/l/email-protection), Guillermo Skrilec: [[email protected]](/cdn-cgi/l/email-protection), Felipe Zipitria: [[email protected]](/cdn-cgi/l/email-protection), Fabien Spychiger: [[email protected]](/cdn-cgi/l/email-protection), Rafael Gil: [[email protected]](/cdn-cgi/l/email-protection), Christian Lopez: [[email protected]](/cdn-cgi/l/email-protection), jonathan fernandez [[email protected]](/cdn-cgi/l/email-protection), Paola Rodriguez: [[email protected]](/cdn-cgi/l/email-protection), Hector Aguirre: [[email protected]](/cdn-cgi/l/email-protection), Roger Carhuatocto: [[email protected]](/cdn-cgi/l/email-protection), Juan Carlos Calderon: [[email protected]](/cdn-cgi/l/email-protection), Marc Rivero López: [[email protected]](/cdn-cgi/l/email-protection), Carlos Allendes: [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection): [[email protected]](/cdn-cgi/l/email-protection), Manuel Ramírez: [[email protected]](/cdn-cgi/l/email-protection), Marco Miranda: [[email protected]](/cdn-cgi/l/email-protection), Mauricio D. Papaleo Mayada: [[email protected]](/cdn-cgi/l/email-protection), Felipe Sanchez: [[email protected]](/cdn-cgi/l/email-protection), Juan Manuel Bahamonde: [[email protected]](/cdn-cgi/l/email-protection), Adrià Massanet: [[email protected]](/cdn-cgi/l/email-protection), Jorge Correa: [[email protected]](/cdn-cgi/l/email-protection), Ramiro Pulgar: [[email protected]](/cdn-cgi/l/email-protection), German Alonso Suárez Guerrero: [[email protected]](/cdn-cgi/l/email-protection), Jose A. Guasch: [[email protected]](/cdn-cgi/l/email-protection), Edgar Salazar: [[email protected]](/cdn-cgi/l/email-protection)
* Ukrainian 2013: [OWASP Top 10 2013 - Ukrainian PDF](https://www.owasp.org/images/e/e3/OWASP_Top_10_-_2013_Final_Ukrainian.pdf)  
  Kateryna Ovechenko, Yuriy Fedko, Gleb Paharenko, Yevgeniya Maskayeva, Sergiy Shabashkevich, Bohdan Serednytsky

### 2010 Completed Translations:

* Korean 2010: [OWASP Top 10 2010 - Korean PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP%20Top%2010%20-%202010%20Korean.pdf)  
  Hyungkeun Park, ([[email protected]](/cdn-cgi/l/email-protection))
* Spanish 2010: [OWASP Top 10 2010 - Spanish PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP%20Top%2010%20-%202010%20Spanish.pdf)  
   Daniel Cabezas Molina, Edgar Sanchez, Juan Carlos Calderon, Jose Antonio Guasch, Paulo Coronado, Rodrigo Marcos, Vicente Aguilera
* French 2010: [OWASP Top 10 2010 - French PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP%20Top%2010%20-%202010%20French.pdf)  
  [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection)
* German 2010: [OWASP Top 10 2010 - German PDF](https://wiki.owasp.org/?title=Special:Redirect/file/OWASPTop10_2010_DE_Version_1_0.pdf)  
  [[email protected]](/cdn-cgi/l/email-protection) which is Frank Dölitzscher, Tobias Glemser, Dr. Ingo Hanke, [Kai Jendrian](https://wiki.owasp.org/index.php/User:Kai_Jendrian), [Ralf Reinhardt](https://wiki.owasp.org/index.php/https://wiki.owasp.org/index.php/User:Ralf_Reinhardt), Michael Schäfer
* Indonesian 2010: [OWASP Top 10 2010 - Indonesian PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP%20Top%2010%20-%202010%20Indonesian.pdf)  
  Tedi Heriyanto (coordinator), Lathifah Arief, Tri A Sundara, Zaki Akhmad
* Italian 2010: [OWASP Top 10 2010 - Italian PDF](https://www.owasp.org/images/f/f9/OWASP_Top_10_-_2010_ITA.pdf)  
  Simone Onofri, Paolo Perego, Massimo Biagiotti, Edoardo Viscosi, Salvatore Fiorillo, Roberto Battistoni, Loredana Mancini, Michele Nesta, Paco Schiaffella, Lucilla Mancini, Gerardo Di Giacomo, Valentino Squilloni
* Japanese 2010: [OWASP Top 10 2010 - Japanese PDF](https://torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASP%20Top%2010%20-%202010%20Japanese-A4.pdf)  
  [[email protected]](/cdn-cgi/l/email-protection), Dr. Masayuki Hisada, Yoshimasa Kawamoto, Ryusuke Sakamoto, Keisuke Seki, Shin Umemoto, Takashi Arima
* Chinese 2010: [OWASP Top 10 2010 - Chinese PDF](https://www.owasp.org/images/a/a9/OWASP_Top_10_2010_Chinese_V1.0_Released.pdf)  
  感谢以下为中文版本做出贡献的翻译人员和审核人员: Rip Torn, 钟卫林, 高雯, 王颉, 于振东
* Vietnamese 2010: [OWASP Top 10 2010 - Vietnamese PDF](torage.googleapis.com/google-code-archive-downloads/v2/code.google.com/owasptop10/OWASPTop%2010%20-%202010%20Vietnamese.pdf)  
  Translation lead by Cecil Su - Translation Team: Dang Hoang Vu, Nguyen Ba Tien, Nguyen Tang Hung, Luong Dieu Phuong, Huynh Thien Tam
* Hebrew 2010: [OWASP Top 10 Hebrew Project](https://wiki.owasp.org/index.php/OWASP_Top10_Hebrew) – [OWASP Top 10 2010 - Hebrew PDF](https://www.owasp.org/images/c/cd/OWASP_Top_10_Heb.pdf).  
  Lead by Or Katz, see translation page for list of contributors.

---

## 2021 Project Sponsors

The OWASP Top 10:2021 is sponsored by Secure Code Warrior.

## 2017 Project Sponsors

The OWASP Top 10 - 2017 project was sponsored by Autodesk, and supported by the [OWASP NoVA Chapter](https://owasp.org/www-chapter-northern-virginia/).

## 2003-2013 Project Sponsors

Thanks to [Aspect Security](https://www.aspectsecurity.com/) for sponsoring earlier versions.

---

# OWASP Top 10 2025 Data Analysis Plan

## Goals

To collect the most comprehensive dataset related to identified application vulnerabilities to-date to enable analysis for the Top 10 and other future research as well. This data should come from a variety of sources; security vendors and consultancies, bug bounties, along with company/organizational contributions. Data will be normalized to allow for level comparison between Human assisted Tooling and Tooling assisted Humans.

## Analysis Infrastructure

Plan to leverage the OWASP Azure Cloud Infrastructure to collect, analyze, and store the data contributed.

## Contributions

We plan to support both known and pseudo-anonymous contributions. The preference is for contributions to be known; this immensely helps with the validation/quality/confidence of the data submitted. If the submitter prefers to have their data stored anonymously and even go as far as submitting the data anonymously, then it will have to be classified as “unverified” vs. “verified”.

### Verified Data Contribution

Scenario 1: The submitter is known and has agreed to be identified as a contributing party.  
Scenario 2: The submitter is known but would rather not be publicly identified.  
Scenario 3: The submitter is known but does not want it recorded in the dataset.

### Unverified Data Contribution

Scenario 4: The submitter is anonymous. (Should we support?)

The analysis of the data will be conducted with a careful distinction when the unverified data is part of the dataset that was analyzed.

## Contribution Process

There are a few ways that data can be contributed:

1. Email a CSV/Excel file with the dataset(s) to [[email protected]](/cdn-cgi/l/email-protection)
2. Upload a CSV/Excel file to <https://bit.ly/OWASPTop10Data>

Template examples can be found in GitHub: <https://github.com/OWASP/Top10/tree/master/2025/Data>

## Contribution Period

We plan to accept contributions to the new Top 10 until July 31, 2025, for data dating from 2021 to 2024.

## Data Structure

The following data elements are **required** or optional.   
The more information provided the more accurate our analysis can be.  
At a bare minimum, we need the time period, total number of applications tested in the dataset, and the list of CWEs and counts of how many applications contained that CWE.  
If at all possible, please provide the additional metadata, because that will greatly help us gain more insights into the current state of testing and vulnerabilities.

### Metadata

* Contributor Name (org or anon)
* Contributor Contact Email
* **Time period (2024, 2023, 2022, 2021)**
* **Number of applications tested**
* Type of testing (TaH, HaT, Tools)
* Primary Language (code)
* Geographic Region (Global, North America, EU, Asia, other)
* Primary Industry (Multiple, Financial, Industrial, Software, ??)
* Whether or not data contains retests or the same applications multiple times (T/F)

### CWE Data

* **A list of CWEs w/ count of applications found to contain that CWE**

*If at all possible, please provide core CWEs in the data, not CWE categories.*  
*This will help with the analysis, any normalization/aggregation done as a part of this analysis will be well documented.*

#### Note:

If a contributor has two types of datasets, one from HaT and one from TaH sources, then it is recommended to submit them as two separate datasets.  
*HaT = Human assisted Tools (higher volume/frequency, primarily from tooling)*  
*TaH = Tool assisted Human (lower volume/frequency, primarily from human testing)*

## Survey

Similarly to the Top Ten 2021, we plan to conduct a survey to identify up to two categories of the Top Ten that the community believes are important, but may not be reflected in the data yet. We plan to conduct the survey in early 2025, and will be utilizing Google forms in a similar manner as last time. The CWEs on the survey will come from current trending findings, CWEs that are outside the Top Ten in data, and other potential sources.

## Process

At a high level, we plan to perform a level of data normalization; however, we will keep a version of the raw data contributed for future analysis. We will analyze the CWE distribution of the datasets and potentially reclassify some CWEs to consolidate them into larger buckets. We will carefully document all normalization actions taken so it is clear what has been done.

We plan to calculate likelihood following the model we continued in 2021 to determine incidence rate instead of frequency to rate how likely a given app may contain at least one instance of a CWE. This means we aren’t looking for the frequency rate (number of findings) in an app, rather, we are looking for the number of applications that had one or more instances of a CWE. We can calculate the incidence rate based on the total number of applications tested in the dataset compared to how many applications each CWE was found in.

In addition, we will be developing base CWSS scores for the top 20-30 CWEs and include potential impact into the Top 10 weighting.

Also, would like to explore additional insights that could be gleaned from the contributed dataset to see what else can be learned that could be of use to the security and development communities.

---

[Watch](https://github.com/owasp/www-project-top-ten/subscription)
[Star](https://github.com/owasp/www-project-top-ten)

**The OWASP® Foundation** works to improve the security of software through its community-led open source software projects,
hundreds of chapters worldwide, tens of thousands of members, and by hosting local and global conferences.

### Project Information

* • [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
* • [Making of OWASP Top 10](https://www.owasptopten.org/)
* Flagship Project
* Documentation
* Builder
* Defender
* • [Previous Version (2021)](https://owasp.org/Top10/2021/)
* • [Previous Version (2017)](2017)

### Downloads or Social Links

* • [OWASP Top 10 2017](/www-pdf-archive/OWASP_Top_10-2017_%28en%29.pdf.pdf)
* • [Other languages → tab ‘Translation Efforts’](/www-project-top-ten/#div-translation_efforts)

### Social

* [Twitter](https://twitter.com/owasptop10)

### Code Repository

* [Github repo](https://github.com/OWASP/Top10)

### Leaders

* [Andrew van der Stock](/cdn-cgi/l/email-protection#6315020d0706110209230c140210134d0c1104)
* [Brian Glas](/cdn-cgi/l/email-protection#bcdeced5ddd292dbd0ddcffcd3cbddcfcc92d3cedb)
* [Neil Smithline](/cdn-cgi/l/email-protection#28464d4144065b45415c404441464d68475f495b5806475a4f)
* [Tanya Janca](/cdn-cgi/l/email-protection#ec988d82958dc2868d828f8dac839b8d9f9cc2839e8b)
* [Torsten Gigler](/cdn-cgi/l/email-protection#4c38233e3f382922622b252b20293e0c233b2d3f3c62233e2b)

### Upcoming OWASP Global Events

var events = [];
$(function () {
eventsyml = YAML.load('https://owasp.org/assets/sitedata/events.yml');
$.each(eventsyml, function (index) {
if (this.category == 'Global') {
for (e in this.events) {
events.push(this.events[e]);
}
}
});
if (events.length > 0) {
var htmlstring = "<ul>";
for (evnt in events) {
if (events[evnt].url)
htmlstring += '<li><a href="' + events[evnt].url
else
htmlstring += '<li><a href="https://owasp.org/events/'
htmlstring += '" target="\_blank rel="noopener">' + events[evnt].name + '</a>';
if (typeof events[evnt].dates === 'undefined') {
events[evnt].dates = 'TBA';
}
htmlstring += "<ul><li style='list-style-type: circle;margin-top: 0px;padding:0px;margin-left:16px;'>" + events[evnt].dates + "</li></ul></li>";
}
htmlstring += "</ul>";
$("#global-event-div").html(htmlstring);
}
});

* [HOME](/)
* [PROJECTS](/projects/)
* [CHAPTERS](/chapters/)
* [EVENTS](/events/)
* [ABOUT](/about/)
* [PRIVACY](/www-policy/operational/privacy)
* [SITEMAP](/sitemap/)
* [CONTACT](/contact/)

Open Web Application Security Project, OWASP, Global AppSec, AppSec Days, AppSec California, SnowFROC, LASCON, and the OWASP logo are trademarks of the OWASP Foundation. Unless otherwise specified, all content on the site is Creative Commons Attribution-ShareAlike v4.0 and provided without warranty of service or accuracy. For more information, please refer to our [General Disclaimer](/www-policy/operational/general-disclaimer.html). OWASP does not endorse or recommend commercial products or services, allowing our community to remain vendor neutral with the collective wisdom of the best minds in software security worldwide. Copyright 2025, OWASP Foundation, Inc.

---

var members = [];
$(function() {
corp\_members = YAML.load('https://owasp.org/assets/sitedata/corp\_members.yml');
$.each(corp\_members, function (index) {
members.push(this);
});
var randomIndexUsed = [];
var counter = 0;
var numberOfImages = 10;
if(members.length > 0)
{
var htmlstring = "";
while (counter < numberOfImages)
{
var randomIndex;
var img;
randomIndex = Math.floor(Math.random() \* members.length);
if (randomIndexUsed.indexOf(randomIndex) == "-1")
{
counter++;
htmlstring += '<a href="'+ members[randomIndex]["url"] + '" class="alt-member-logo" rel="sponsored noopener noreferrer" target="\_blank" onclick="handleOutboundLinkClicks(event);"><img src="https://owasp.org' + members[randomIndex]["image"] + '" alt="image"/></a>';
randomIndexUsed.push(randomIndex);
}
}
$("#corp\_member\_div").html(htmlstring);
}
});

## A selection of our Corporate Supporters

[Become a corporate supporter](/supporters)