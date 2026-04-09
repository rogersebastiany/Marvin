(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Create a console app – tutorial | Kotlin Documentation[{"id":"create-a-project","level":0,"title":"Create a project","anchor":"#create-a-project"},{"id":"create-an-application","level":0,"title":"Create an application","anchor":"#create-an-application"},{"id":"run-the-application","level":0,"title":"Run the application","anchor":"#run-the-application"},{"id":"what-s-next","level":0,"title":"What\u0027s next?","anchor":"#what-s-next"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/jvm-get-started.html#webpage",
"url": "https://kotlinlang.org/docs/jvm-get-started.html",
"name": "Create a console app &ndash; tutorial | Kotlin",
"description": "",
"image": "https://kotlinlang.org/assets/images/open-graph/docs.png",
"inLanguage":"en-US"
}{
"@type": "WebSite",
"@id": "https://kotlinlang.org/docs/#website",
"url": "https://kotlinlang.org/docs/",
"name": "Kotlin Help"
}a[href="test-page.html"] { visibility: hidden; }

### Kotlin Help

# Create a console app – tutorial

This tutorial demonstrates how to use IntelliJ IDEA for creating a console application.

To get started, first download and install the latest version of [IntelliJ IDEA](https://www.jetbrains.com/idea/download/).

## Create a project

1. In IntelliJ IDEA, select File | New | Project.
2. In the list on the left, select Kotlin.
3. Name the new project and change its location if necessary.

   Select the Create Git repository checkbox to place the new project under version control. You will be able to do it later at any time.
4. Select the IntelliJ build system. It's a native builder that doesn't require downloading additional artifacts.

   If you want to create a more complex project that needs further configuration, select Maven or Gradle. For Gradle, choose a language for the build script: Kotlin or Groovy.
5. From the JDK list, select the [JDK](https://www.oracle.com/java/technologies/downloads/) that you want to use in your project.

   * If the JDK is installed on your computer, but not defined in the IDE, select Add JDK and specify the path to the JDK home directory.
   * If you don't have the necessary JDK on your computer, select Download JDK.
6. Enable the Add sample code option to create a file with a sample `"Hello World!"` application.

   You can also enable the Generate code with onboarding tips option to add some additional useful comments to your sample code.
7. Click Create.

   If you chose the Gradle build system, you have in your project a build script file: `build.gradle(.kts)`. It includes the `kotlin("jvm")` plugin and dependencies required for your console application. Make sure that you use the latest version of the plugin:

   plugins {
   kotlin("jvm") version "2.3.20"
   application
   }

   plugins {
   id 'org.jetbrains.kotlin.jvm' version '2.3.20'
   id 'application'
   }

## Create an application

1. Open the `Main.kt` file in `src/main/kotlin`.   
    The `src` directory contains Kotlin source files and resources. The `Main.kt` file contains sample code that will print `Hello, Kotlin!` as well as several lines with values of the cycle iterator.
2. Modify the code so that it requests your name and says `Hello` to you:

   * Create an input prompt and assign to the `name` variable the value returned by the [`readln()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.io/readln.html) function.
   * Let's use a string template instead of concatenation by adding a dollar sign `$` before the variable name directly in the text output like this – `$name`.

   fun main() {
   println("What's your name?")
   val name = readln()
   println("Hello, $name!")
   // ...
   }

## Run the application

Now the application is ready to run. The easiest way to do this is to click the green Run icon in the gutter and select Run 'MainKt'.

You can see the result in the Run tool window.

Enter your name and accept the greetings from your application!

Congratulations! You have just run your first Kotlin application.

## What's next?

Once you've created this application, you can start to dive deeper into Kotlin syntax:

* Take the [Kotlin tour](kotlin-tour-welcome.html)
* Install the [JetBrains Academy plugin](https://plugins.jetbrains.com/plugin/10081-jetbrains-academy) for IDEA and complete exercises from the [Kotlin Koans course](https://plugins.jetbrains.com/plugin/10081-jetbrains-academy/docs/learner-start-guide.html?section=Kotlin%20Koans)

16 March 2026

[Kotlin command-line compiler](command-line.html)[Kotlin compiler options](compiler-reference.html)