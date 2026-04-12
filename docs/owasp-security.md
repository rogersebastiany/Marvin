# OWASP Security


---

## 1. SQL Injection Prevention Cheat Sheet

## Introduction

This cheat sheet will help you prevent SQL injection flaws in your applications. It will define what SQL injection is, explain where those flaws occur, and provide four options for defending against SQL injection attacks. [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) attacks are common because:

1. SQL Injection vulnerabilities are very common.
2. The application's database is a frequent target for attackers because it typically contains sensitive or critical data.

## What Is a SQL Injection Attack?

Attackers can use SQL injection on an application if it has dynamic database queries that use string concatenation and user-supplied input. To avoid SQL injection flaws, developers need to:

1. Stop writing dynamic queries with string concatenation.
2. Prevent malicious SQL input from being included in executed queries.

There are simple techniques for preventing SQL injection vulnerabilities, and they can be used with practically any kind of programming language and any type of database. While XML databases can have similar problems (e.g., XPath and XQuery injection), these techniques can be used to protect them as well.

## Anatomy of a Typical SQL Injection Vulnerability

A common SQL injection flaw in Java is shown below. Because its unvalidated "customerName" parameter is simply appended to the query, an attacker can enter SQL code into that query and the application would take the attacker's code and execute it on the database.

```
Stringquery="SELECT account_balance FROM user_data WHERE user_name = "
+request.getParameter("customerName");
try{
Statementstatement=connection.createStatement(...);
ResultSetresults=statement.executeQuery(query);
}

...
```

## Primary Defenses

* **Option 1: Use of Prepared Statements (with Parameterized Queries)**
* **Option 2: Use of Properly Constructed Stored Procedures**
* **Option 3: Allow-list Input Validation**
* **Option 4: STRONGLY DISCOURAGED: Escaping All User Supplied Input**

### Defense Option 1: Prepared Statements (with Parameterized Queries)

When developers are taught how to write database queries, they should be told to use prepared statements with variable binding (aka parameterized queries). Prepared statements are simple to write and easier to understand than dynamic queries, and parameterized queries force the developer to define all SQL code first and pass in each parameter to the query later.

If database queries use this coding style, the database will always distinguish between code and data, regardless of what user input is supplied. Also, prepared statements ensure that an attacker cannot change the intent of a query, even if SQL commands are inserted by an attacker.

#### Safe Java Prepared Statement Example

In the safe Java example below, if an attacker were to enter the userID as `tom' or '1'='1`, the parameterized query would look for a username that literally matches the entire string `tom' or '1'='1`. Thus, the database would be protected against injections of malicious SQL code.

The following code example uses a `PreparedStatement`, Java's implementation of a parameterized query, to execute the same database query.

```
// This should REALLY be validated too
Stringcustname=request.getParameter("customerName");
// Perform input validation to detect attacks
Stringquery="SELECT account_balance FROM user_data WHERE user_name = ? ";
PreparedStatementpstmt=connection.prepareStatement(query);
pstmt.setString(1,custname);
ResultSetresults=pstmt.executeQuery();
```

#### Safe C# .NET Prepared Statement Example

In .NET, the creation and execution of the query doesn't change. Just pass the parameters to the query using the `Parameters.Add()` call as shown below.

```
Stringquery="SELECT account_balance FROM user_data WHERE user_name = ?";
try{
OleDbCommandcommand=newOleDbCommand(query,connection);
command.Parameters.Add(newOleDbParameter("customerName",CustomerNameName.Text));
OleDbDataReaderreader=command.ExecuteReader();
// …
}catch(OleDbExceptionse){
// error handling
}
```

While we have shown examples in Java and .NET, practically all other languages (including Cold Fusion and Classic ASP) support parameterized query interfaces. Even SQL abstraction layers, like the [Hibernate Query Language](http://hibernate.org/) (HQL) with the same type of injection problems (called [HQL Injection](http://cwe.mitre.org/data/definitions/564.html)) support parameterized queries as well:

#### Hibernate Query Language (HQL) Prepared Statement (Named Parameters) Example

```
// This is an unsafe HQL statement
QueryunsafeHQLQuery=session.createQuery("from Inventory where productID='"+userSuppliedParameter+"'");
// Here is a safe version of the same query using named parameters
QuerysafeHQLQuery=session.createQuery("from Inventory where productID=:productid");
safeHQLQuery.setParameter("productid",userSuppliedParameter);
```

#### Other Examples of Safe Prepared Statements

If you need examples of prepared queries/parameterized languages, including Ruby, PHP, Cold Fusion, Perl, and Rust, see the [Query Parameterization Cheat Sheet](Query_Parameterization_Cheat_Sheet.html) or this [site](http://bobby-tables.com/).

Generally, developers like prepared statements because all the SQL code stays within the application, which makes applications relatively database independent.

### Defense Option 2: Stored Procedures

Though stored procedures are not always safe from SQL injection, developers can use certain standard stored procedure programming constructs. This approach has the same effect as using parameterized queries, as long as the stored procedures are implemented safely (which is the norm for most stored procedure languages).

#### Safe Approach to Stored Procedures

If stored procedures are needed, the safest approach to using them requires the developer to build SQL statements with parameters that are automatically parameterized, unless the developer does something largely out of the norm. The difference between prepared statements and stored procedures is that the SQL code for a stored procedure is defined and stored in the database itself, then called from the application. Since prepared statements and safe stored procedures are equally effective in preventing SQL injection, your organization should choose the approach that makes the most sense for you.

#### When Stored Procedures Can Increase Risk

Occasionally, stored procedures can increase risk when a system is attacked. For example, on MS SQL Server, you have three main default roles: `db_datareader`, `db_datawriter` and `db_owner`. Before stored procedures came into use, DBAs would give `db_datareader` or `db_datawriter` rights to the webservice's user, depending on the requirements.

However, stored procedures require execute rights, a role not available by default. In some setups where user management has been centralized, but is limited to those 3 roles, web apps would have to run as `db_owner` so stored procedures could work. Naturally, that means that if a server is breached, the attacker has full rights to the database, where previously, they might only have had read-access.

#### Safe Java Stored Procedure Example

The following code example uses Java's implementation of the stored procedure interface (`CallableStatement`) to execute the same database query. The `sp_getAccountBalance` stored procedure has to be predefined in the database and use the same functionality as the query above.

```
// This should REALLY be validated
Stringcustname=request.getParameter("customerName");
try{
CallableStatementcs=connection.prepareCall("{call sp_getAccountBalance(?)}");
cs.setString(1,custname);
ResultSetresults=cs.executeQuery();
// … result set handling
}catch(SQLExceptionse){
// … logging and error handling
}
```

#### Safe VB .NET Stored Procedure Example

The following code example uses a `SqlCommand`, .NET's implementation of the stored procedure interface, to execute the same database query. The `sp_getAccountBalance` stored procedure must be predefined in the database and use the same functionality as the query defined above.

```
Try
DimcommandAsSqlCommand=newSqlCommand("sp_getAccountBalance",connection)
command.CommandType=CommandType.StoredProcedure
command.Parameters.Add(newSqlParameter("@CustomerName",CustomerName.Text))
DimreaderAsSqlDataReader=command.ExecuteReader()
'...
CatchseAsSqlException
'error handling
EndTry
```

### Defense Option 3: Allow-list Input Validation

If you are faced with parts of SQL queries that can't use bind variables, such as table names, column names, or sort order indicators (ASC or DESC), input validation or query redesign is the most appropriate defense. When table or column names are needed, ideally those values come from the code and not from user parameters.

#### Sample Of Safe Table Name Validation

WARNING: Using user parameter values to target table or column names is a symptom of poor design and a full rewrite should be considered if time allows. If that is not possible, developers should map the parameter values to the legal/expected table or column names to make sure unvalidated user input doesn't end up in the query.

In the example below, since `tableName` is identified as one of the legal and expected values for a table name in this query, it can be directly appended to the SQL query. Keep in mind that generic table validation functions can lead to data loss if table names are used in queries where they are not expected.

```
String tableName;
switch(PARAM):
  case "Value1": tableName = "fooTable";
                 break;
  case "Value2": tableName = "barTable";
                 break;
  ...
  default      : throw new InputValidationException("unexpected value provided"
                                                  + " for table name");
```

#### Safest Use Of Dynamic SQL Generation (DISCOURAGED)

When we say a stored procedure is "implemented safely," that means it does not include any unsafe dynamic SQL generation. Developers do not usually generate dynamic SQL inside stored procedures. However, it can be done, but should be avoided.

If it can't be avoided, the stored procedure must use input validation or proper escaping, as described in this article, to make sure that all user supplied input to the stored procedure can't be used to inject SQL code into the dynamically generated query. Auditors should always look for uses of `sp_execute`, `execute` or `exec` within SQL Server stored procedures. Similar audit guidelines are necessary for similar functions for other vendors.

#### Sample of Safer Dynamic Query Generation (DISCOURAGED)

For something simple like a sort order, it is best if the user supplied input is converted to a boolean, and then that boolean is used to select the safe value to append to the query. This is a very standard need in dynamic query creation.

For example:

```
publicStringsomeMethod(booleansortOrder){
StringSQLquery="some SQL ... order by Salary "+(sortOrder?"ASC":"DESC");`
...
```

Any time user input can be converted to a non-String, like a date, numeric, boolean, enumerated type, etc. before it is appended to a query, or used to select a value to append to the query, this ensures it is safe to do so.

Input validation is also recommended as a secondary defense in ALL cases, even when using bind variables as discussed earlier in this article. More techniques on how to implement strong input validation is described in the [Input Validation Cheat Sheet](Input_Validation_Cheat_Sheet.html).

### Defense Option 4: STRONGLY DISCOURAGED: Escaping All User-Supplied Input

In this approach, the developer will escape all user input before putting it in a query. It is very database specific in its implementation. This methodology is fragile compared to other defenses, and we CANNOT guarantee that this option will prevent all SQL injections in all situations.

If an application is built from scratch or requires low risk tolerance, it should be built or re-written using parameterized queries, stored procedures, or some kind of Object Relational Mapper (ORM) that builds your queries for you.

## Additional Defenses

Beyond adopting one of the four primary defenses, we also recommend adopting all of these additional defenses to provide defense in depth. These additional defenses are:

* **Least Privilege**
* **Allow-list Input Validation**

### Least Privilege

To minimize the potential damage of a successful SQL injection attack, you should minimize the privileges assigned to every database account in your environment. Start from the ground up to determine what access rights your application accounts require, rather than trying to figure out what access rights you need to take away.

Make sure that accounts that only need read access are only granted read access to the tables they need access to. DO NOT ASSIGN DBA OR ADMIN TYPE ACCESS TO YOUR APPLICATION ACCOUNTS. We understand that this is easy, and everything just "works" when you do it this way, but it is very dangerous.

#### Minimizing Application and OS Privileges

SQL injection is not the only threat to your database data. Attackers can simply change the parameter values from one of the legal values they are presented with, to a value that is unauthorized for them, but the application itself might be authorized to access. As such, minimizing the privileges granted to your application will reduce the likelihood of such unauthorized access attempts, even when an attacker is not trying to use SQL injection as part of their exploit.

While you are at it, you should minimize the privileges of the operating system account that the DBMS runs under. Don't run your DBMS as root or system! Most DBMSs run out of the box with a very powerful system account. For example, MySQL runs as system on Windows by default! Change the DBMS's OS account to something more appropriate, with restricted privileges.

#### Details Of Least Privilege When Developing

If an account only needs access to portions of a table, consider creating a view that limits access to that portion of the data and assigning the account access to the view instead of the underlying table. Rarely, if ever, grant create or delete access to database accounts.

If you adopt a policy where you use stored procedures everywhere, and don't allow application accounts to directly execute their own queries, then restrict those accounts to only be able to execute the stored procedures they need. Don't grant them any rights directly to the tables in the database.

#### Least Admin Privileges For Multiple DBs

The designers of web applications should avoid using the same owner/admin account in the web applications to connect to the database. Different DB users should be used for different web applications.

In general, each separate web application that requires access to the database should have a designated database user account that the application will use to connect to the DB. That way, the designer of the application can have good granularity in the access control, thus reducing the privileges as much as possible. Each DB user will then have select access to only what it needs, and write-access as needed.

As an example, a login page requires read access to the username and password fields of a table, but no write access of any form (no insert, update, or delete). However, the sign-up page certainly requires insert privilege to that table; this restriction can only be enforced if these web apps use different DB users to connect to the database.

#### Enhancing Least Privilege with SQL Views

You can use SQL views to further increase the granularity of access by limiting the read access to specific fields of a table or joins of tables. It could have additional benefits.

For example, if the system is required (perhaps due to some specific legal requirements) to store the passwords of the users, instead of salted-hashed passwords, the designer could use views to compensate for this limitation. They could revoke all access to the table (from all DB users except the owner/admin) and create a view that outputs the hash of the password field and not the field itself.

Any SQL injection attack that succeeds in stealing DB information will be restricted to stealing the hash of the passwords (could even be a keyed hash), since no DB user for any of the web applications has access to the table itself.

### Allow-list Input Validation

In addition to being a primary defense when nothing else is possible (e.g., when a bind variable isn't legal), input validation can also be a secondary defense used to detect unauthorized input before it is passed to the SQL query. For more information please see the [Input Validation Cheat Sheet](Input_Validation_Cheat_Sheet.html). Proceed with caution here. Validated data is not necessarily safe to insert into SQL queries via string building.

## Related Articles

**SQL Injection Attack Cheat Sheets**:

The following articles describe how to exploit different kinds of SQL injection vulnerabilities on various platforms (that this article was created to help you avoid):

* [SQL Injection Cheat Sheet](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/)
* Bypassing WAF's with SQLi - [SQL Injection Bypassing WAF](https://owasp.org/www-community/attacks/SQL_Injection_Bypassing_WAF)

**Description of SQL Injection Vulnerabilities**:

* OWASP article on [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) Vulnerabilities
* OWASP article on [Blind\_SQL\_Injection](https://owasp.org/www-community/attacks/Blind_SQL_Injection) Vulnerabilities

**How to Avoid SQL Injection Vulnerabilities**:

* [OWASP Developers Guide](https://github.com/OWASP/DevGuide) article on how to avoid SQL injection vulnerabilities
* OWASP Cheat Sheet that provides [numerous language specific examples of parameterized queries using both Prepared Statements and Stored Procedures](Query_Parameterization_Cheat_Sheet.html)
* [The Bobby Tables site (inspired by the XKCD webcomic) has numerous examples in different languages of parameterized Prepared Statements and Stored Procedures](http://bobby-tables.com/)

**How to Review Code for SQL Injection Vulnerabilities**:

* [OWASP Code Review Guide](https://wiki.owasp.org/index.php/Category:OWASP_Code_Review_Project) article on how to [Review Code for SQL Injection](https://wiki.owasp.org/index.php/Reviewing_Code_for_SQL_Injection) Vulnerabilities

**How to Test for SQL Injection Vulnerabilities**:

* [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide) article on how to [Test for SQL Injection](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.html) Vulnerabilities

---

## 2. Input Validation Cheat Sheet

## Introduction

This article is focused on providing clear, simple, actionable guidance for providing Input Validation security functionality in your applications.

## Goals of Input Validation

Input validation is performed to ensure only properly formed data is entering the workflow in an information system, preventing malformed data from persisting in the database and triggering malfunction of various downstream components. Input validation should happen as early as possible in the data flow, preferably as soon as the data is received from the external party.

Data from all potentially untrusted sources should be subject to input validation, including not only Internet-facing web clients but also backend feeds over extranets, from [suppliers, partners, vendors or regulators](https://badcyber.com/several-polish-banks-hacked-information-stolen-by-unknown-attackers/), each of which may be compromised on their own and start sending malformed data.

Input Validation should not be used as the *primary* method of preventing [XSS](Cross_Site_Scripting_Prevention_Cheat_Sheet.html), [SQL Injection](SQL_Injection_Prevention_Cheat_Sheet.html) and other attacks which are covered in respective [cheat sheets](https://cheatsheetseries.owasp.org/) but can significantly contribute to reducing their impact if implemented properly.

## Input Validation Strategies

Input validation should be applied at both syntactic and semantic levels:

* **Syntactic** validation should enforce correct syntax of structured fields (e.g. SSN, date, currency symbol).
* **Semantic** validation should enforce correctness of their *values* in the specific business context (e.g. start date is before end date, price is within expected range).

It is always recommended to prevent attacks as early as possible in the processing of the user's (attacker's) request. Input validation can be used to detect unauthorized input before it is processed by the application.

## Implementing Input Validation

Input validation can be implemented using any programming technique that allows effective enforcement of syntactic and semantic correctness, for example:

* Data type validators available natively in web application frameworks (such as [Django Validators](https://docs.djangoproject.com/en/1.11/ref/validators/), [Apache Commons Validators](https://commons.apache.org/proper/commons-validator/apidocs/org/apache/commons/validator/package-summary.html#doc.Usage.validator) etc).
* Validation against [JSON Schema](http://json-schema.org/) and [XML Schema (XSD)](https://www.w3schools.com/xml/schema_intro.asp) for input in these formats.
* Type conversion (e.g. `Integer.parseInt()` in Java, `int()` in Python) with strict exception handling
* Minimum and maximum value range check for numerical parameters and dates, minimum and maximum length check for strings.
* Array of allowed values for small sets of string parameters (e.g. days of week).
* Regular expressions for any other structured data covering the whole input string `(^...$)` and **not** using "any character" wildcard (such as `.` or `\S`)
* Denylisting known dangerous patterns can be used as an additional layer of defense, but it should supplement - not replace - allowlisting, to help catch some commonly observed attacks or patterns without relying on it as the main validation method.

### Allowlist vs Denylist

It is a common mistake to use denylist validation in order to try to detect possibly dangerous characters and patterns like the apostrophe `'` character, the string `1=1`, or the `<script>` tag, but this is a massively flawed approach as it is trivial for an attacker to bypass such filters.

Plus, such filters frequently prevent authorized input, like `O'Brian`, where the `'` character is fully legitimate. For more information on XSS filter evasion please see [this wiki page](https://owasp.org/www-community/xss-filter-evasion-cheatsheet).

While denylisting can be useful as an additional layer of defense to catch some common malicious patterns, it should not be relied upon as the primary method. Allowlisting remains the more robust and secure approach for preventing potentially harmful input.

Allowlist validation is appropriate for all input fields provided by the user. Allowlist validation involves defining exactly what IS authorized, and by definition, everything else is not authorized.

If it's well structured data, like dates, social security numbers, zip codes, email addresses, etc. then the developer should be able to define a very strong validation pattern, usually based on regular expressions, for validating such input.

If the input field comes from a fixed set of options, like a drop down list or radio buttons, then the input needs to match exactly one of the values offered to the user in the first place. Any failure to validate a value against this discrete list of options on the server side is a high security event and should be logged as a high severity event as it indicates that an attacker is tampering with the client-side code.

### Validating Free-form Unicode Text

Free-form text, especially with Unicode characters, is perceived as difficult to validate due to a relatively large space of characters that need to be allowed.

It's also free-form text input that highlights the importance of proper context-aware output encoding and quite clearly demonstrates that input validation is **not** the primary safeguards against Cross-Site Scripting. If your users want to type apostrophe `'` or less-than sign `<` in their comment field, they might have perfectly legitimate reason for that and the application's job is to properly handle it throughout the whole life cycle of the data.

The primary means of input validation for free-form text input should be:

* **Normalization:** Ensure canonical encoding is used across all the text and no invalid characters are present.
* **Character category allowlisting:** Unicode allows listing categories such as "decimal digits" or "letters" which not only covers the Latin alphabet but also various other scripts used globally (e.g. Arabic, Cyrillic, CJK ideographs etc).
* **Individual character allowlisting:** If you allow letters and ideographs in names and also want to allow apostrophe `'` for Irish names, but don't want to allow the whole punctuation category.

References:

* [Input validation of free-form Unicode text in Python](https://web.archive.org/web/20170717174432/https://ipsec.pl/python/2017/input-validation-free-form-unicode-text-python.html/)
* [UAX 31: Unicode Identifier and Pattern Syntax](https://unicode.org/reports/tr31/)
* [UAX 15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/)
* [UAX 24: Unicode Script Property](https://unicode.org/reports/tr24/)

### Regular Expressions (Regex)

Developing regular expressions can be complicated, and is well beyond the scope of this cheat sheet.

There are lots of resources on the internet about how to write regular expressions, including this [site](https://www.regular-expressions.info/) and the [OWASP Validation Regex Repository](https://owasp.org/www-community/OWASP_Validation_Regex_Repository).

When designing regular expression, be aware of [RegEx Denial of Service (ReDoS) attacks](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS). These attacks cause a program using a poorly designed Regular Expression to operate very slowly and utilize CPU resources for a very long time.

In summary, input validation should:

* Be applied to all input data, at minimum.
* Define the allowed set of characters to be accepted.
* Define a minimum and maximum length for the data (e.g. `{1,25}`).

## Allow List Regular Expression Examples

Validating a U.S. Zip Code (5 digits plus optional -4)

```
^\d{5}(-\d{4})?$
```

Validating U.S. State Selection From a Drop-Down Menu

```
^(AA|AE|AP|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|
HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|
NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|
TX|UT|VT|VI|VA|WA|WV|WI|WY)$
```

**Java Regex Usage Example:**

Example validating the parameter "zip" using a regular expression.

```
privatestaticfinalPatternzipPattern=Pattern.compile("^\d{5}(-\d{4})?$");

publicvoiddoPost(HttpServletRequestrequest,HttpServletResponseresponse){
try{
StringzipCode=request.getParameter("zip");
if(!zipPattern.matcher(zipCode).matches()){
thrownewYourValidationException("Improper zipcode format.");
}
// do what you want here, after its been validated ..
}catch(YourValidationExceptione){
response.sendError(response.SC_BAD_REQUEST,e.getMessage());
}
}
```

Some Allowlist validators have also been predefined in various open source packages that you can leverage. For example:

* [Apache Commons Validator](http://commons.apache.org/proper/commons-validator/)

## Client-side vs Server-side Validation

Input validation **must** be implemented on the server-side before any data is processed by an application’s functions, as any JavaScript-based input validation performed on the client-side can be circumvented by an attacker who disables JavaScript or uses a web proxy. Implementing both client-side JavaScript-based validation for UX and server-side validation for security is the recommended approach, leveraging each for their respective strengths.

## Validating Rich User Content

It is very difficult to validate rich content submitted by a user. For more information, please see the XSS cheat sheet on [Sanitizing HTML Markup with a Library Designed for the Job](Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

## Preventing XSS and Content Security Policy

All user data controlled must be encoded when returned in the HTML page to prevent the execution of malicious data (e.g. XSS). For example `<script>` would be returned as `&lt;script&gt;`

The type of encoding is specific to the context of the page where the user controlled data is inserted. For example, HTML entity encoding is appropriate for data placed into the HTML body. However, user data placed into a script would need JavaScript specific output encoding.

Detailed information on XSS prevention here: [OWASP XSS Prevention Cheat Sheet](Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

## File Upload Validation

Many websites allow users to upload files, such as a profile picture or more. This section helps provide that feature securely.

Check the [File Upload Cheat Sheet](File_Upload_Cheat_Sheet.html).

### Upload Verification

* Use input validation to ensure the uploaded filename uses an expected extension type.
* Ensure the uploaded file is not larger than a defined maximum file size.
* If the website supports ZIP file upload, do a validation check before unzipping the file. The check includes the target path, level of compression, estimated unzip size.

### Upload Storage

* Use a new filename to store the file on the OS. Do not use any user controlled text for this filename or for the temporary filename.
* When the file is uploaded to web, it's suggested to rename the file on storage. For example, the uploaded filename is *test.JPG*, rename it to *JAI1287uaisdjhf.JPG* with a random filename. The purpose of doing it to prevent the risks of direct file access and ambiguous filename to evade the filter, such as `test.jpg;.asp or /../../../../../test.jpg`.
* Uploaded files should be analyzed for malicious content (anti-malware, static analysis, etc).
* The client should not be able to specify the file path; it should be defined by the server.

### Public Serving of Uploaded Content

* Ensure uploaded images are served with the correct content-type (e.g. `image/jpeg`, `application/x-xpinstall`)

### Beware of Specific File Types

The upload feature should be using an allowlist approach to only allow specific file types and extensions. However, it is important to be aware of the following file types that, if allowed, could result in security vulnerabilities:

* **crossdomain.xml** / **clientaccesspolicy.xml:** allows cross-domain data loading in Flash, Java and Silverlight. If permitted on sites with authentication this can permit cross-domain data theft and CSRF attacks. Note this can get pretty complicated depending on the specific plugin version in question, so its best to just prohibit files named "crossdomain.xml" or "clientaccesspolicy.xml".
* **.htaccess** and **.htpasswd:** Provides server configuration options on a per-directory basis, and should not be permitted. See [HTACCESS documentation](https://en.wikipedia.org/wiki/Htaccess).
* Web executable script files are suggested not to be allowed such as `aspx, asp, css, swf, xhtml, rhtml, shtml, jsp, js, pl, php, cgi`.

### Image Upload Verification

* Use image rewriting libraries to verify the image is valid and to strip away extraneous content.
* Set the extension of the stored image to be a valid image extension based on the detected content type of the image from image processing (e.g. do not just trust the header from the upload).
* Ensure the detected content type of the image is within a list of defined image types (jpg, PNG, etc)

## Email Address Validation

### Syntactic Validation

The format of email addresses is defined by [RFC 5321](https://tools.ietf.org/html/rfc5321#section-4.1.2), and is far more complicated than most people realise. As an example, the following are all considered to be valid email addresses:

* `"><script>alert(1);</script>"@example.org`
* `[email protected]`
* `user@[IPv6:2001:db8::1]`
* `" "@example.org`

Properly parsing email addresses for validity with regular expressions is very complicated, although there are a number of [publicly available documents on regex](https://datatracker.ietf.org/doc/html/draft-seantek-mail-regexen-03#rfc.section.3).

The biggest caveat on this is that although the RFC defines a very flexible format for email addresses, most real world implementations (such as mail servers) use a far more restricted address format, meaning that they will reject addresses that are *technically* valid. Although they may be technically correct, these addresses are of little use if your application will not be able to actually send emails to them.

As such, the best way to validate email addresses is to perform some basic initial validation, and then pass the address to the mail server and catch the exception if it rejects it. This means that the application can be confident that its mail server can send emails to any addresses it accepts. The initial validation could be as simple as:

* The email address contains two parts, separated with an `@` symbol.
* The email address does not contain dangerous characters (such as backticks, single or double quotes, or null bytes).
  + Exactly which characters are dangerous will depend on how the address is going to be used (echoed in page, inserted into database, etc).
* The domain part contains only letters, numbers, hyphens (`-`) and periods (`.`).
* The email address is a reasonable length:
  + The local part (before the `@`) should be no more than 63 characters.
  + The total length should be no more than 254 characters.

### Semantic Validation

Semantic validation is about determining whether the email address is correct and legitimate. The most common way to do this is to send an email to the user, and require that they click a link in the email, or enter a code that has been sent to them. This provides a basic level of assurance that:

* The email address is correct.
* The application can successfully send emails to it.
* The user has access to the mailbox.

The links that are sent to users to prove ownership should contain a token that is:

* At least 32 characters long.
* Generated using a [secure source of randomness](Cryptographic_Storage_Cheat_Sheet.html#secure-random-number-generation).
* Single use.
* Time limited (e.g, expiring after eight hours).

After validating the ownership of the email address, the user should then be required to authenticate on the application through the usual mechanism.

#### Disposable Email Addresses

In some cases, users may not want to give their real email address when registering on the application, and will instead provide a disposable email address. These are publicly available addresses that do not require the user to authenticate, and are typically used to reduce the amount of spam received by users' primary email addresses.

Blocking disposable email addresses is almost impossible, as there are a large number of websites offering these services, with new domains being created every day. There are a number of publicly available lists and commercial lists of known disposable domains, but these will always be incomplete.

If these lists are used to block the use of disposable email addresses then the user should be presented with a message explaining why they are blocked (although they are likely to simply search for another disposable provider rather than giving their legitimate address).

If it is essential that disposable email addresses are blocked, then registrations should only be allowed from specifically-allowed email providers. However, if this includes public providers such as Google or Yahoo, users can simply register their own disposable address with them.

#### Sub-Addressing

Sub-addressing allows a user to specify a *tag* in the local part of the email address (before the `@` sign), which will be ignored by the mail server. For example, if that `example.org` domain supports sub-addressing, then the following email addresses are equivalent:

* `[email protected]`
* `[email protected]`
* `[email protected]`

Many mail providers (such as Microsoft Exchange) do not support sub-addressing. The most notable provider who does is Gmail, although there are many others that also do.

Some users will use a different *tag* for each website they register on, so that if they start receiving spam to one of the sub-addresses they can identify which website leaked or sold their email address.

Because it could allow users to register multiple accounts with a single email address, some sites may wish to block sub-addressing by stripping out everything between the `+` and `@` signs. This is not generally recommended, as it suggests that the website owner is either unaware of sub-addressing or wishes to prevent users from identifying them when they leak or sell email addresses. Additionally, it can be trivially bypassed by using [disposable email addresses](#disposable-email-addresses), or simply registering multiple email accounts with a trusted provider.

## References

* [OWASP Top 10 Proactive Controls 2024: C3: Validate all Input & Handle Exceptions](https://top10proactive.owasp.org/the-top-10/c3-validate-input-and-handle-exceptions)
* [CWE-20 Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
* [OWASP Top 10 2021: A03:2021-Injection](https://owasp.org/Top10/A03_2021-Injection/)
* [Snyk: Improper Input Validation](https://learn.snyk.io/lesson/improper-input-validation/)

---

## 3. REST Security Cheat Sheet

## Introduction

[REST](https://en.wikipedia.org/wiki/REST) (or **RE**presentational **S**tate **T**ransfer) is an architectural style first described in [Roy Fielding](https://en.wikipedia.org/wiki/Roy_Fielding)'s Ph.D. dissertation on [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).

It evolved as Fielding wrote the HTTP/1.1 and URI specs and has been proven to be well-suited for developing distributed hypermedia applications. While REST is more widely applicable, it is most commonly used within the context of communicating with services via HTTP.

The key abstraction of information in REST is a resource. A REST API resource is identified by a URI, usually a HTTP URL. REST components use connectors to perform actions on a resource by using a representation to capture the current or intended state of the resource and transferring that representation.

The primary connector types are client and server, secondary connectors include cache, resolver and tunnel.

REST APIs are stateless. Stateful APIs do not adhere to the REST architectural style. State in the REST acronym refers to the state of the resource which the API accesses, not the state of a session within which the API is called. While there may be good reasons for building a stateful API, it is important to realize that managing sessions is complex and difficult to do securely.

Stateful services are out of scope of this Cheat Sheet: *Passing state from client to backend, while making the service technically stateless, is an anti-pattern that should also be avoided as it is prone to replay and impersonation attacks.*

In order to implement flows with REST APIs, resources are typically created, read, updated and deleted. For example, an ecommerce site may offer methods to create an empty shopping cart, to add items to the cart and to check out the cart. Each of these REST calls is stateless and the endpoint should check whether the caller is authorized to perform the requested operation.

Another key feature of REST applications is the use of standard HTTP verbs and error codes in the pursuit or removing unnecessary variation among different services.

Another key feature of REST applications is the use of [HATEOAS or Hypermedia As The Engine of Application State](https://en.wikipedia.org/wiki/HATEOAS). This provides REST applications a self-documenting nature making it easier for developers to interact with a REST service without prior knowledge.

## HTTPS

Secure REST services must only provide HTTPS endpoints. This protects authentication credentials in transit, for example passwords, API keys or JSON Web Tokens. It also allows clients to authenticate the service and guarantees integrity of the transmitted data.

See the [Transport Layer Security Cheat Sheet](Transport_Layer_Security_Cheat_Sheet.html) for additional information.

Consider the use of mutually authenticated client-side certificates to provide additional protection for highly privileged web services.

## Access Control

Non-public REST services must perform access control at each API endpoint. Web services in monolithic applications implement this by means of user authentication, authorization logic and session management. This has several drawbacks for modern architectures which compose multiple microservices following the RESTful style.

* in order to minimize latency and reduce coupling between services, the access control decision should be taken locally by REST endpoints
* user authentication should be centralised in a Identity Provider (IdP), which issues access tokens

## JWT

There seems to be a convergence towards using [JSON Web Tokens](https://tools.ietf.org/html/rfc7519) (JWT) as the format for security tokens. JWTs are JSON data structures containing a set of claims that can be used for access control decisions. A cryptographic signature or message authentication code (MAC) can be used to protect the integrity of the JWT.

* Ensure JWTs are integrity protected by either a signature or a MAC. Do not allow the unsecured JWTs: `{"alg":"none"}`.
  + See [here](https://tools.ietf.org/html/rfc7519#section-6.1)
* In general, signatures should be preferred over MACs for integrity protection of JWTs.

If MACs are used for integrity protection, every service that is able to validate JWTs can also create new JWTs using the same key. This means that all services using the same key have to mutually trust each other. Another consequence of this is that a compromise of any service also compromises all other services sharing the same key. See [here](https://tools.ietf.org/html/rfc7515#section-10.5) for additional information.

The relying party or token consumer validates a JWT by verifying its integrity and claims contained.

* A relying party must verify the integrity of the JWT based on its own configuration or hard-coded logic. It must not rely on the information of the JWT header to select the verification algorithm. See [here](https://www.chosenplaintext.ca/2015/03/31/jwt-algorithm-confusion.html) and [here](https://www.youtube.com/watch?v=bW5pS4e_MX8>)

Some claims have been standardized and should be present in JWT used for access controls. At least the following of the standard claims should be verified:

* `iss` or issuer - is this a trusted issuer? Is it the expected owner of the signing key?
* `aud` or audience - is the relying party in the target audience for this JWT?
* `exp` or expiration time - is the current time before the end of the validity period of this token?
* `nbf` or not before time - is the current time after the start of the validity period of this token?

As JWTs contain details of the authenticated entity (user etc.) a disconnect can occur between the JWT and the current state of the users session, for example, if the session is terminated earlier than the expiration time due to an explicit logout or an idle timeout. When an explicit session termination event occurs, a digest or hash of any associated JWTs should be submitted to a denylist on the API which will invalidate that JWT for any requests until the expiration of the token. See the [JSON\_Web\_Token\_for\_Java\_Cheat\_Sheet](JSON_Web_Token_for_Java_Cheat_Sheet.html#token-explicit-revocation-by-the-user) for further details.

## API Keys

Public REST services without access control run the risk of being farmed leading to excessive bills for bandwidth or compute cycles. API keys can be used to mitigate this risk. They are also often used by organisation to monetize APIs; instead of blocking high-frequency calls, clients are given access in accordance to a purchased access plan.

API keys can reduce the impact of denial-of-service attacks. However, when they are issued to third-party clients, they are relatively easy to compromise.

* Require API keys for every request to the protected endpoint.
* Return `429 Too Many Requests` HTTP response code if requests are coming in too quickly.
* Revoke the API key if the client violates the usage agreement.
* Do not rely exclusively on API keys to protect sensitive, critical or high-value resources.

## Restrict HTTP methods

* Apply an allowlist of permitted HTTP Methods e.g. `GET`, `POST`, `PUT`.
* Reject all requests not matching the allowlist with HTTP response code `405 Method not allowed`.
* Make sure the caller is authorised to use the incoming HTTP method on the resource collection, action, and record

In Java EE in particular, this can be difficult to implement properly. See [Bypassing Web Authentication and Authorization with HTTP Verb Tampering](../assets/REST_Security_Cheat_Sheet_Bypassing_VBAAC_with_HTTP_Verb_Tampering.pdf) for an explanation of this common misconfiguration.

## Preventing Out-of-Order API Execution

Modern REST APIs often implement business workflows through a sequence of endpoints (for example, create → validate → approve → finalize). If the backend does not explicitly validate workflow state transitions, attackers may invoke endpoints out of sequence to bypass intended controls.

### Problem

Out-of-order API execution occurs when an attacker:

* Skips required workflow steps by directly calling later-stage endpoints
* Replays or reuses tokens across workflow boundaries
* Exploits assumptions that the frontend enforces correct sequencing

Because each endpoint may be individually authenticated and authorized, traditional access control checks often fail to detect these issues.

### Example

A checkout workflow expects the following sequence:

```
POST /checkout/create
POST /checkout/pay
POST /checkout/confirm
```

If the backend does not validate workflow state transitions, an attacker could directly invoke:

```
POST /checkout/confirm
```

without completing payment.

### Prevention Guidance

* Enforce workflow state validation on the server side for every request
* Model workflows explicitly using finite states or state machines
* Bind tokens or identifiers to specific workflow stages
* Avoid relying on frontend logic to enforce sequencing
* Reject invalid or out-of-order transitions with clear error responses

### Testing Checklist

* Can endpoints be invoked out of sequence?
* Does each endpoint validate the current workflow state?
* Are tokens reusable across workflow steps?
* Are invalid state transitions consistently rejected?

## Input validation

* Do not trust input parameters/objects.
* Validate input: length / range / format and type.
* Achieve an implicit input validation by using strong types like numbers, booleans, dates, times or fixed data ranges in API parameters.
* Constrain string inputs with regexps.
* Reject unexpected/illegal content.
* Make use of validation/sanitation libraries or frameworks in your specific language.
* Define an appropriate request size limit and reject requests exceeding the limit with HTTP response status 413 Request Entity Too Large.
* Consider logging input validation failures. Assume that someone who is performing hundreds of failed input validations per second is up to no good.
* Have a look at input validation cheat sheet for comprehensive explanation.
* Use a secure parser for parsing the incoming messages. If you are using XML, make sure to use a parser that is not vulnerable to [XXE](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_%28XXE%29_Processing) and similar attacks.

## Validate content types

A REST request or response body should match the intended content type in the header. Otherwise this could cause misinterpretation at the consumer/producer side and lead to code injection/execution.

* Document all supported content types in your API.

### Validate request content types

* Reject requests containing unexpected or missing content type headers with HTTP response status `406 Unacceptable` or `415 Unsupported Media Type`. For requests with `Content-Length: 0` however, a `Content-type` header is optional.
* For XML content types ensure appropriate XML parser hardening, see the [XXE cheat sheet](XML_External_Entity_Prevention_Cheat_Sheet.html).
* Avoid accidentally exposing unintended content types by explicitly defining content types e.g. [Jersey](https://jersey.github.io/) (Java) `@consumes("application/json"); @produces("application/json")`. This avoids [XXE-attack](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_%28XXE%29_Processing) vectors for example.

### Send safe response content types

It is common for REST services to allow multiple response types (e.g. `application/xml` or `application/json`, and the client specifies the preferred order of response types by the Accept header in the request.

* **Do NOT** simply copy the `Accept` header to the `Content-type` header of the response.
* Reject the request (ideally with a `406 Not Acceptable` response) if the `Accept` header does not specifically contain one of the allowable types.

Services including script code (e.g. JavaScript) in their responses must be especially careful to defend against header injection attack.

* Ensure sending intended content type headers in your response matching your body content e.g. `application/json` and not `application/javascript`.

## Management endpoints

* Avoid exposing management endpoints via Internet.
* If management endpoints must be accessible via the Internet, make sure that users must use a strong authentication mechanism, e.g. multi-factor.
* Expose management endpoints via different HTTP ports or hosts preferably on a different NIC and restricted subnet.
* Restrict access to these endpoints by firewall rules or use of access control lists.

## Error handling

* Respond with generic error messages - avoid revealing details of the failure unnecessarily.
* Do not pass technical details (e.g. call stacks or other internal hints) to the client.

## Audit logs

* Write audit logs before and after security related events.
* Consider logging token validation errors in order to detect attacks.
* Take care of log injection attacks by sanitizing log data beforehand.

## Security Headers

There are a number of [security related headers](https://owasp.org/www-project-secure-headers/) that can be returned in the HTTP responses to instruct browsers to act in specific ways. However, some of these headers are intended to be used with HTML responses, and as such may provide little or no security benefits on an API that does not return HTML. Note that if the API is only consumed by non-browser clients (e.g. mobile apps, server-to-server calls, command-line tools), most of these headers will have no effect since they are directives for browsers.

The following headers should be included in all API responses that may be consumed by browser clients:

| Header | Rationale |
| --- | --- |
| `Cache-Control: no-store` | Header used to direct caching done by browsers. Providing `no-store` indicates that any caches of any kind (private or shared) should not store the response that contains the header. A browser must make a new request everytime the API is called to fetch the latest response. This header with a `no-store` value prevents sensitive information from being cached or stored. |
| `Content-Security-Policy: frame-ancestors 'none'` | Header used to specify whether a response can be framed in a `<frame>`, `<iframe>`, `<embed>` or `<object>` element. For an API response, there is no requirement to be framed in any of those elements. Providing `frame-ancestors 'none'` prevents any domain from framing the response returned by the API call. This header protects against [drag-and-drop](https://www.w3.org/Security/wiki/Clickjacking_Threats#Drag_and_drop_attacks) style clickjacking attacks. |
| `Content-Type` | Header to specify the content type of a response. This must be specified as per the type of content returned by an API call. If not specified or if specified incorrectly, a browser might attempt to guess the content type of the response. This can return in MIME sniffing attacks. One common content type value is `application/json` if the API response is JSON. |
| `Strict-Transport-Security` | Header to instruct a browser that the domain should only be accessed using HTTPS, and that any future attempts to access it using HTTP should automatically be converted to HTTPS. This header ensures that API calls are made over HTTPS and protects against spoofed certificates. |
| `X-Content-Type-Options: nosniff` | Header to instruct a browser to always use the MIME type that is declared in the `Content-Type` header rather than trying to determine the MIME type based on the file's content. This header with a `nosniff` value prevents browsers from performing MIME sniffing, and inappropriately interpreting responses as HTML. |
| `X-Frame-Options: DENY` | Legacy header superseded by `Content-Security-Policy: frame-ancestors 'none'` (see above). Still recommended for compatibility with older browsers that do not support CSP Level 2. Providing `DENY` prevents any domain from framing the response. |

The headers below are only intended to provide additional security when responses are rendered as HTML. As such, if the API will **never** return HTML in responses, then these headers may not be necessary. However, if there is any uncertainty about the function of the headers, or the types of information that the API returns (or may return in future), then it is recommended to include them as part of a defence-in-depth approach.

| Header | Example | Rationale |
| --- | --- | --- |
| Content-Security-Policy | `Content-Security-Policy: default-src 'none'` | The majority of CSP functionality only affects pages rendered as HTML. |
| Permissions-Policy | `Permissions-Policy: accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), cross-origin-isolated=(), display-capture=(), document-domain=(), encrypted-media=(), execution-while-not-rendered=(), execution-while-out-of-viewport=(), fullscreen=(), geolocation=(), gyroscope=(), keyboard-map=(), magnetometer=(), microphone=(), midi=(), navigation-override=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), sync-xhr=(), usb=(), web-share=(), xr-spatial-tracking=()` | This header used to be named Feature-Policy. When browsers heed this header, it is used to control browser features via directives. The example disables features with an empty allowlist for a number of permitted [directive names](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy#directives). When you apply this header, verify that the directives are up-to-date and fit your needs. Please have a look at this [article](https://developer.chrome.com/en/docs/privacy-sandbox/permissions-policy) for a detailed explanation on how to control browser features. |
| Referrer-Policy | `Referrer-Policy: no-referrer` | Non-HTML responses should not trigger additional requests. |

## CORS

Cross-Origin Resource Sharing (CORS) is a W3C standard to flexibly specify what cross-domain requests are permitted. By delivering appropriate CORS Headers your REST API signals to the browser which domains, AKA origins, are allowed to make JavaScript calls to the REST service.

* Disable CORS headers if cross-domain calls are not supported/expected.
* Be as specific as possible and as general as necessary when setting the origins of cross-domain calls.

## Sensitive information in HTTP requests

RESTful web services should be careful to prevent leaking credentials. Passwords, security tokens, and API keys should not appear in the URL, as this can be captured in web server logs, which makes them intrinsically valuable.

* In `POST`/`PUT` requests sensitive data should be transferred in the request body or request headers.
* In `GET` requests sensitive data should be transferred in an HTTP Header.

**OK:**

`https://example.com/resourceCollection/[ID]/action`

`https://twitter.com/vanderaj/lists`

**NOT OK:**

`https://example.com/controller/123/action?apiKey=a53f435643de32` because the apiKey is in the URL.

## HTTP Return Code

HTTP defines [status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). When designing REST API, don't just use `200` for success or `404` for error. Always use the semantically appropriate status code for the response.

Here is a non-exhaustive selection of security related REST API **status codes**. Use it to ensure you return the correct code.

| Code | Message | Description |
| --- | --- | --- |
| 200 | OK | Response to a successful REST API action. The HTTP method can be GET, POST, PUT, PATCH or DELETE. |
| 201 | Created | The request has been fulfilled and resource created. A URI for the created resource is returned in the Location header. |
| 202 | Accepted | The request has been accepted for processing, but processing is not yet complete. |
| 301 | Moved Permanently | Permanent redirection. |
| 304 | Not Modified | Caching related response that returned when the client has the same copy of the resource as the server. |
| 307 | Temporary Redirect | Temporary redirection of resource. |
| 400 | Bad Request | The request is malformed, such as message body format error. |
| 401 | Unauthorized | Wrong or no authentication ID/password provided. |
| 403 | Forbidden | It's used when the authentication succeeded but authenticated user doesn't have permission to the request resource. |
| 404 | Not Found | When a non-existent resource is requested. |
| 405 | Method Not Acceptable | The error for an unexpected HTTP method. For example, the REST API is expecting HTTP GET, but HTTP PUT is used. |
| 406 | Unacceptable | The client presented a content type in the Accept header which is not supported by the server API. |
| 413 | Payload too large | Use it to signal that the request size exceeded the given limit e.g. regarding file uploads. |
| 415 | Unsupported Media Type | The requested content type is not supported by the REST service. |
| 429 | Too Many Requests | The error is used when there may be DOS attack detected or the request is rejected due to rate limiting. |
| 500 | Internal Server Error | An unexpected condition prevented the server from fulfilling the request. Be aware that the response should not reveal internal information that helps an attacker, e.g. detailed error messages or stack traces. |
| 501 | Not Implemented | The REST service does not implement the requested operation yet. |
| 503 | Service Unavailable | The REST service is temporarily unable to process the request. Used to inform the client it should retry at a later time. |

Additional information about HTTP return code usage in REST API can be found [here](https://www.restapitutorial.com/httpstatuscodes.html) and [here](https://restfulapi.net/http-status-codes).

---

## 4. OWASP Top Ten Web Application Security Risks

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

---

## 5. Authentication Cheat Sheet

## Introduction

**Authentication** (**AuthN**) is the process of verifying that an individual, entity, or website is who or what it claims to be by determining the validity of one or more authenticators (like passwords, fingerprints, or security tokens) that are used to back up this claim.

**Digital Identity** is the unique representation of a subject engaged in an online transaction. A digital identity is always unique in the context of a digital service but does not necessarily need to be traceable back to a specific real-life subject.

**Identity Proofing** establishes that a subject is actually who they claim to be. This concept is related to KYC concepts and it aims to bind a digital identity with a real person.

**Session Management** is a process by which a server maintains the state of an entity interacting with it. This is required for a server to remember how to react to subsequent requests throughout a transaction. Sessions are maintained on the server by a session identifier which can be passed back and forth between the client and server when transmitting and receiving requests. Sessions should be unique per user and computationally very difficult to predict. The [Session Management Cheat Sheet](Session_Management_Cheat_Sheet.html) contains further guidance on the best practices in this area.

## Authentication General Guidelines

### User IDs

The primary function of a User ID is to uniquely identify a user within a system. Ideally, User IDs should be randomly generated to prevent the creation of predictable or sequential IDs, which could pose a security risk, especially in systems where User IDs might be exposed or inferred from external sources.

### Usernames

Usernames are easy-to-remember identifiers chosen by the user and used for identifying themselves when logging into a system or service. The terms User ID and username might be used interchangeably if the username chosen by the user also serves as their unique identifier within the system.

Users should be permitted to use their email address as a username, provided the email is verified during sign-up. Additionally, they should have the option to choose a username other than an email address. For information on validating email addresses, please visit the [input validation cheat sheet email discussion](Input_Validation_Cheat_Sheet.html#email-address-validation).

### Authentication Solution and Sensitive Accounts

* Do **NOT** allow login with sensitive accounts (i.e. accounts that can be used internally within the solution such as to a backend / middleware / database) to any front-end user interface
* Do **NOT** use the same authentication solution (e.g. IDP / AD) used internally for unsecured access (e.g., public access / DMZ)

### Implement Proper Password Strength Controls

A key concern when using passwords for authentication is password strength. A "strong" password policy makes it difficult or even improbable for one to guess the password through either manual or automated means. The following characteristics define a strong password:

* Password Length
  + **Minimum** length for passwords should be enforced by the application.
    - If MFA is enabled passwords **shorter than 8 characters** are considered to be weak ([NIST SP800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)).
    - If MFA is not enabled passwords **shorter than 15 characters** are considered to be weak ([NIST SP800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)).
  + **Maximum** password length should be **at least 64 characters** to allow passphrases ([NIST SP800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)). Note that certain implementations of hashing algorithms may cause [long password denial of service](https://www.acunetix.com/vulnerabilities/web/long-password-denial-of-service/).
* Do not silently truncate passwords. The [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.html#maximum-password-lengths) provides further guidance on how to handle passwords that are longer than the maximum length.
* Allow usage of **all** characters including unicode and whitespace. There should be no password composition rules limiting the type of characters permitted. There should be no requirement for upper or lower case or numbers or special characters.
* Ensure credential rotation when a password leak occurs, at the time of compromise identification or when authenticator technology changes. Avoid requiring periodic password changes; instead, encourage users to pick strong passwords and enable [Multifactor Authentication Cheat Sheet (MFA)](Multifactor_Authentication_Cheat_Sheet.html). According to NIST guidelines, verifiers should not mandate arbitrary password changes (e.g., periodically).
* Include a password strength meter to help users create a more complex password
  + [zxcvbn-ts library](https://github.com/zxcvbn-ts/zxcvbn) can be used for this purpose.
  + Other language implementations of zxcvbn [listed here](https://github.com/dropbox/zxcvbn?tab=readme-ov-file); however check the age and maturity of each example before use.
* Block common and previously breached passwords
  + [Pwned Passwords](https://haveibeenpwned.com/Passwords) is a service where passwords can be checked against previously breached passwords. Details on the API [are here](https://haveibeenpwned.com/API/v3#PwnedPasswords).
  + Alternatively, you can download the [Pwned Passwords](https://haveibeenpwned.com/Passwords) database [using this mechanism](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader?tab=readme-ov-file#what-is-haveibeenpwned-downloader) to host it yourself.
  + Other top password lists are available but there is no guarantee as to how updated they are:
    - [Various password lists](https://github.com/danielmiessler/SecLists/tree/master/Passwords) hosted by SecLists from Daniel Miessler.
    - Static copy of the top 100,000 passwords from "Have I Been Pwned" hosted by NCSC in [text](https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.txt) and [JSON](https://www.ncsc.gov.uk/static-assets/documents/PwnedPasswordsTop100k.json) format.

#### For more detailed information check

* [ASVS v5.0 Password Security Requirements](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md#v62-password-security)
* [Passwords Evolved: Authentication Guidance for the Modern Era](https://www.troyhunt.com/passwords-evolved-authentication-guidance-for-the-modern-era/)

### Implement Secure Password Recovery Mechanism

It is common for an application to have a mechanism that provides a means for a user to gain access to their account in the event they forget their password. Please see [Forgot Password Cheat Sheet](Forgot_Password_Cheat_Sheet.html) for details on this feature.

### Store Passwords in a Secure Fashion

It is critical for an application to store a password using the right cryptographic technique. Please see [Password Storage Cheat Sheet](Password_Storage_Cheat_Sheet.html) for details on this feature.

### Compare Password Hashes Using Safe Functions

Where possible, the user-supplied password should be compared to the stored password hash using a secure password comparison function provided by the language or framework, such as the [password\_verify()](https://www.php.net/manual/en/function.password-verify.php) function in PHP. Where this is not possible, ensure that the comparison function:

* Has a maximum input length, to protect against denial of service attacks with very long inputs.
* Explicitly sets the type of both variables, to protect against type confusion attacks such as Magic Hashes in PHP.
* Returns in constant time, to protect against timing attacks.

### Change Password Feature

When developing a change password feature, ensure to have:

* The user is authenticated with an active session.
* Current password verification. This is to ensure that it's the legitimate user who is changing the password. Consider this abuse case: a user logs in on a public computer and forgets to log out. Another person could then use that active session. If we don't verify the current password, this other person may be able to change the password.

### Transmit Passwords Only Over TLS or Other Strong Transport

See: [Transport Layer Security Cheat Sheet](Transport_Layer_Security_Cheat_Sheet.html)

The login page and all subsequent authenticated pages must be exclusively accessed over TLS or other strong transport. Failure to utilize TLS or other strong transport for the login page allows an attacker to modify the login form action, causing the user's credentials to be posted to an arbitrary location. Failure to utilize TLS or other strong transport for authenticated pages after login enables an attacker to view the unencrypted session ID and compromise the user's authenticated session.

### Require Re-authentication for Sensitive Features

In order to mitigate CSRF and session hijacking, it's important to require the current credentials for an account before updating sensitive account information such as the user's password or email address -- or before sensitive transactions, such as shipping a purchase to a new address. Without this countermeasure, an attacker may be able to execute sensitive transactions through a CSRF or XSS attack without needing to know the user's current credentials. Additionally, an attacker may get temporary physical access to a user's browser or steal their session ID to take over the user's session.

### Reauthentication After Risk Events

**Overview:**
Reauthentication is critical when an account has experienced high-risk activity such as account recovery, password resets, or suspicious behavior patterns. This section outlines when and how to trigger reauthentication to protect users and prevent unauthorized access. For further details, see the [Require Re-authentication for Sensitive Features](#require-re-authentication-for-sensitive-features) section.

#### When to Trigger Reauthentication

* **Suspicious Account Activity**
  When unusual login patterns, IP address changes, or device enrollments occur
* **Account Recovery**
  After users reset their passwords or change sensitive account details
* **Critical Actions**
  For high-risk actions like changing payment details or adding new trusted devices

#### Reauthentication Mechanisms

* **Adaptive Authentication**
  Use risk-based authentication models that adapt to the user's behavior and context
* **Multi-Factor Authentication (MFA)**
  Require an additional layer of verification for sensitive actions or events
* **Challenge-Based Verification**
  Prompt users to confirm their identity with a challenge question or secondary method

#### Implementation Recommendations

* **Minimize User Friction**
  Ensure that reauthentication does not disrupt the user experience unnecessarily
* **Context-Aware Decisions**
  Make reauthentication decisions based on context (e.g., geolocation, device type, prior patterns)
* **Secure Session Management**
  Invalidate sessions after reauthentication and rotate tokens—see the [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

#### References

* [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
* OWASP ASVS – 2.2.2: Reauthentication requirements
* NIST 800-63B: Digital Identity Guidelines – Authentication Assurance Levels

### Consider Strong Transaction Authentication

Some applications should use a second factor to check whether a user may perform sensitive operations. For more information, see the [Transaction Authorization Cheat Sheet](Transaction_Authorization_Cheat_Sheet.html).

#### TLS Client Authentication

TLS Client Authentication, also known as two-way TLS authentication, consists of both browser and server sending their respective TLS certificates during the TLS handshake process. Just as you can validate the authenticity of a server by using the certificate and asking a verifiably-valid Certificate Authority (CA) if the certificate is valid, the server can authenticate the user by receiving a certificate from the client and validating against a third-party CA or its own CA. To do this, the server must provide the user with a certificate generated specifically for him, assigning values to the subject so that these can be used to determine what user the certificate should validate. The user installs the certificate on a browser and now uses it for the website.

This approach is appropriate when:

* It is acceptable (or even preferred) that the user has access to the website only from a single computer/browser.
* The user is not easily scared by the process of installing TLS certificates on their browser, or there will be someone, probably from IT support, who will do this for the user.
* The website requires an extra step of security.
* It is also a good thing to use when the website is for an intranet of a company or organization.

It is generally not a good idea to use this method for widely and publicly available websites that will have an average user. For example, it wouldn't be a good idea to implement this for a website like Facebook. While this technique can prevent the user from having to type a password (thus protecting against an average keylogger from stealing it), it is still considered a good idea to consider using both a password and TLS client authentication combined.

Additionally, if the client is behind an enterprise proxy that performs SSL/TLS decryption, this will break certificate authentication unless the site is allowed on the proxy.

For more information, see: [Client-authenticated TLS handshake](https://en.wikipedia.org/wiki/Transport_Layer_Security#Client-authenticated_TLS_handshake)

### Authentication and Error Messages

Incorrectly implemented error messages in the case of authentication functionality can be used for the purposes of user ID and password enumeration. An application should respond (both HTTP and HTML) in a generic manner.

#### Authentication Responses

Using any of the authentication mechanisms (login, password reset, or password recovery), an application must respond with a generic error message regardless of whether:

* The user ID or password was incorrect.
* The account does not exist.
* The account is locked or disabled.

The account registration feature should also be taken into consideration, and the same approach of a generic error message can be applied regarding the case in which the user exists.

The objective is to prevent the creation of a [discrepancy factor](https://cwe.mitre.org/data/definitions/204.html), allowing an attacker to mount a user enumeration action against the application.

It is interesting to note that the business logic itself can bring a discrepancy factor related to the processing time taken. Indeed, depending on the implementation, the processing time can be significantly different according to the case (success vs failure) allowing an attacker to mount a [time-based attack](https://en.wikipedia.org/wiki/Timing_attack) (delta of some seconds for example).

Example using pseudo-code for a login feature:

* First implementation using the "quick exit" approach

```
IF USER_EXISTS(username) THEN
    password_hash=HASH(password)
    IS_VALID=LOOKUP_CREDENTIALS_IN_STORE(username, password_hash)
    IF NOT IS_VALID THEN
        RETURN Error("Invalid Username or Password!")
    ENDIF
ELSE
   RETURN Error("Invalid Username or Password!")
ENDIF
```

It can be clearly seen that if the user doesn't exist, the application will directly throw an error. Otherwise, when the user exists and the password doesn't, it is apparent that there will be more processing before the application errors out. In return, the response time will be different for the same error, allowing the attacker to differentiate between a wrong username and a wrong password.

* Second implementation without relying on the "quick exit" approach:

```
password_hash=HASH(password)
IS_VALID=LOOKUP_CREDENTIALS_IN_STORE(username, password_hash)
IF NOT IS_VALID THEN
   RETURN Error("Invalid Username or Password!")
ENDIF
```

This code will go through the same process no matter what the user or the password is, allowing the application to return in approximately the same response time.

The problem with returning a generic error message for the user is a User Experience (UX) matter. A legitimate user might feel confused with the generic messages, thus making it hard for them to use the application, and might after several retries, leave the application because of its complexity. The decision to return a *generic error message* can be determined based on the criticality of the application and its data. For example, for critical applications, the team can decide that under the failure scenario, a user will always be redirected to the support page and a *generic error message* will be returned.

Regarding the user enumeration itself, protection against [brute-force attacks](#protect-against-automated-attacks) is also effective because it prevents an attacker from applying the enumeration at scale. Usage of [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) can be applied to a feature for which a *generic error message* cannot be returned because the *user experience* must be preserved.

##### Incorrect and correct response examples

###### Login

Incorrect response examples:

* "Login for User foo: invalid password."
* "Login failed, invalid user ID."
* "Login failed; account disabled."
* "Login failed; this user is not active."

Correct response example:

* "Login failed; Invalid user ID or password."

###### Password recovery

Incorrect response examples:

* "We just sent you a password reset link."
* "This email address doesn't exist in our database."

Correct response example:

* "If that email address is in our database, we will send you an email to reset your password."

###### Account creation

Incorrect response examples:

* "This user ID is already in use."
* "Welcome! You have signed up successfully."

Correct response example:

* "A link to activate your account has been emailed to the address provided."

##### Error Codes and URLs

The application may return a different [HTTP Error code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) depending on the authentication attempt response. It may respond with a 200 for a positive result and a 403 for a negative result. Even though a generic error page is shown to a user, the HTTP response code may differ which can leak information about whether the account is valid or not.

Error disclosure can also be used as a discrepancy factor, consult the [error handling cheat sheet](Error_Handling_Cheat_Sheet.html) regarding the global handling of different errors in an application.

### Protect Against Automated Attacks

There are a number of different types of automated attacks that attackers can use to try and compromise user accounts. The most common types are listed below:

| Attack Type | Description |
| --- | --- |
| Brute Force | Testing multiple passwords from a dictionary or other source against a single account. |
| Credential Stuffing | Testing username/password pairs obtained from the breach of another site. |
| Password Spraying | Testing a single weak password against a large number of different accounts. |

Different protection mechanisms can be implemented to protect against these attacks. In many cases, these defenses do not provide complete protection, but when a number of them are implemented in a defense-in-depth approach, a reasonable level of protection can be achieved.

The following sections will focus primarily on preventing brute-force attacks, although these controls can also be effective against other types of attacks. For further guidance on defending against credential stuffing and password spraying, see the [Credential Stuffing Cheat Sheet](Credential_Stuffing_Prevention_Cheat_Sheet.html).

#### Multi-Factor Authentication

Multi-factor authentication (MFA) is by far the best defense against the majority of password-related attacks, including brute-force attacks, with analysis by Microsoft suggesting that it would have stopped [99.9% of account compromises](https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Your-Pa-word-doesn-t-matter/ba-p/731984). As such, it should be implemented wherever possible; however, depending on the audience of the application, it may not be practical or feasible to enforce the use of MFA.

The [Multifactor Authentication Cheat Sheet](Multifactor_Authentication_Cheat_Sheet.html) contains further guidance on implementing MFA.

#### Login Throttling

Login Throttling is a protocol used to prevent an attacker from making too many attempts at guessing a password through normal interactive means, it includes the following controls:

* Maximum number of attempts.

##### Account Lockout

The most common protection against these attacks is to implement account lockout, which prevents any more login attempts for a period after a certain number of failed logins.

The counter of failed logins should be associated with the account itself, rather than the source IP address, in order to prevent an attacker from making login attempts from a large number of different IP addresses. There are a number of different factors that should be considered when implementing an account lockout policy in order to find a balance between security and usability:

* The number of failed attempts before the account is locked out (lockout threshold).
* The time period that these attempts must occur within (observation window).
* How long the account is locked out for (lockout duration).

Rather than implementing a fixed lockout duration (e.g., ten minutes), some applications use an exponential lockout, where the lockout duration starts as a very short period (e.g., one second), but doubles after each failed login attempt.

* Amount of time to delay after each account lockout (max 2-3, after that permanent account lockout).

When designing an account lockout system, care must be taken to prevent it from being used to cause a denial of service by locking out other users' accounts. One way this could be performed is to allow the use of the forgotten password functionality to log in, even if the account is locked out.

#### CAPTCHA

The use of an effective CAPTCHA can help to prevent automated login attempts against accounts. However, many CAPTCHA implementations have weaknesses that allow them to be solved using automated techniques or can be outsourced to services that can solve them. As such, the use of CAPTCHA should be viewed as a defense-in-depth control to make brute-force attacks more time-consuming and expensive, rather than as a preventative.

It may be more user-friendly to only require a CAPTCHA be solved after a small number of failed login attempts, rather than requiring it from the very first login.

#### Security Questions and Memorable Words

The addition of a security question or memorable word can also help protect against automated attacks, especially when the user is asked to enter a number of randomly chosen characters from the word. It should be noted that this does **not** constitute multi-factor authentication, as both factors are the same (something you know). Furthermore, security questions are often weak and have predictable answers, so they must be carefully chosen. The [Choosing and Using Security Questions cheat sheet](Choosing_and_Using_Security_Questions_Cheat_Sheet.html) contains further guidance on this.

## Logging and Monitoring

Enable logging and monitoring of authentication functions to detect attacks/failures on a real-time basis

* Ensure that all failures are logged and reviewed
* Ensure that all password failures are logged and reviewed
* Ensure that all account lockouts are logged and reviewed

## Use of authentication protocols that require no password

While authentication through a combination of username, password, and multi-factor authentication is considered generally secure, there are use cases where it isn't considered the best option or even safe. Examples of this are third-party applications that desire to connect to the web application, either from a mobile device, another website, desktop, or other situations. When this happens, it is NOT considered safe to allow the third-party application to store the user/password combo, since then it extends the attack surface into their hands, where it isn't in your control. For this and other use cases, there are several authentication protocols that can protect you from exposing your users' data to attackers.

### OAuth 2.0 and 2.1

OAuth is an **authorization** framework for delegated access to APIs. See also: [OAuth 2.0 Cheat Sheet](OAuth2_Cheat_Sheet.html).

> **Note:** OAuth 2.1 is an IETF Working Group draft that consolidates OAuth 2.0 and widely adopted best practices and is intended to replace RFC 6749/6750; guidance in this cheat sheet applies to both OAuth 2.0 and OAuth 2.1. References: [draft-ietf-oauth-v2-1-13](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13), [oauth.net/2.1](https://oauth.net/2.1/)

### OpenID Connect (OIDC)

**OpenID Connect 1.0 (OIDC)** is an identity layer **on top of OAuth**. It defines how a client (**relying party**) verifies the **end user's** identity using an **ID Token** (a signed JWT) and how to obtain user claims in an interoperable way. Use **OIDC for authentication/SSO**; use **OAuth for authorization** to APIs.

#### OIDC implementation guidance

* **Validate ID Tokens** on the relying party: issuer (`iss`), audience (`aud`), signature (per provider JWKs), expiration (`exp`).
* Prefer **well-maintained libraries/SDKs** and provider discovery/JWKS endpoints.
* Use the **UserInfo** endpoint when additional claims beyond the ID Token are required.

> **Avoid confusion:** **OpenID 2.0 ("OpenID")** was a separate, legacy authentication protocol that has been **superseded by OpenID Connect** and is considered obsolete. New systems should not implement OpenID 2.0. References: [OpenID Foundation — obsolete OpenID 2.0 libraries](https://openid.net/developers/libraries-for-obsolete-specifications/), [OpenID 2.0 → OIDC migration](https://openid.net/specs/openid-connect-migration-1_0.html)

### SAML

Security Assertion Markup Language (SAML) is often considered to compete with OpenId. The most recommended version is 2.0 since it is very feature-complete and provides strong security. Like OpenId, SAML uses identity providers, but unlike OpenId, it is XML-based and provides more flexibility. SAML is based on browser redirects which send XML data. Furthermore, SAML isn't only initiated by a service provider; it can also be initiated from the identity provider. This allows the user to navigate through different portals while still being authenticated without having to do anything, making the process transparent.

While OpenId has taken most of the consumer market, SAML is often the choice for enterprise applications because there are few OpenId identity providers which are considered enterprise-class (meaning that the way they validate the user identity doesn't have high standards required for enterprise identity). It is more common to see SAML being used inside of intranet websites, sometimes even using a server from the intranet as the identity provider.

In the past few years, applications like SAP ERP and SharePoint (SharePoint by using Active Directory Federation Services 2.0) have decided to use SAML 2.0 authentication as an often preferred method for single sign-on implementations whenever enterprise federation is required for web services and web applications.

**See also: [SAML Security Cheat Sheet](SAML_Security_Cheat_Sheet.html)**

### FIDO

The Fast Identity Online (FIDO) Alliance has created two protocols to facilitate online authentication: the Universal Authentication Framework (UAF) protocol and the Universal Second Factor (U2F) protocol. While UAF focuses on passwordless authentication, U2F allows the addition of a second factor to existing password-based authentication. Both protocols are based on a public key cryptography challenge-response model.

UAF takes advantage of existing security technologies present on devices for authentication including fingerprint sensors, cameras (face biometrics), microphones (voice biometrics), Trusted Execution Environments (TEEs), Secure Elements (SEs), and others. The protocol is designed to plug these device capabilities into a common authentication framework. UAF works with both native applications and web applications.

U2F augments password-based authentication using a hardware token (typically USB) that stores cryptographic authentication keys and uses them for signing. The user can use the same token as a second factor for multiple applications. U2F works with web applications. It provides **protection against phishing** by using the URL of the website to look up the stored authentication key.

**FIDO2**: FIDO2 and WebAuthn, encompassing previous standards (UAF/U2F), form the foundation of modern **Passkeys** technology. Passkeys enable users to securely log in using local user verification (such as biometrics or device PINs) and often supporting cloud synchronization across devices. This technology is widely supported by major platforms. (Windows Hello/Mac Touch ID)

## Password Managers

Password managers are programs, browser plugins, or web services that automate the management of a large quantity of different credentials. Most password managers have functionality to allow users to easily use them on websites, either:
(a) by pasting the passwords into the login form
-- or --
(b) by simulating the user typing them in.

Web applications should not make the job of password managers more difficult than necessary by observing the following recommendations:

* Use standard HTML forms for username and password input with appropriate `type` attributes.
* Avoid plugin-based login pages (such as Flash or Silverlight).
* Implement a reasonable maximum password length, at least 64 characters, as discussed in the [Implement Proper Password Strength Controls section](#implement-proper-password-strength-controls).
* Allow any printable characters to be used in passwords.
* Allow users to paste into the username, password, and MFA fields.
* Allow users to navigate between the username and password field with a single press of the `Tab` key.

## Changing A User's Registered Email Address

User email addresses often change. The following process is recommended to handle such situations in a system:

*Note: The process is less stringent with [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html), as proof-of-identity is stronger than relying solely on a password.*

### Recommended Process If the User HAS [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) Enabled

1. Confirm the validity of the user's authentication cookie/token. If not valid, display a login screen.
2. Describe the process for changing the registered email address to the user.
3. Ask the user to submit a proposed new email address, ensuring it complies with system rules.
4. Request the use of [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) for identity verification.
5. Store the proposed new email address as a pending change.
6. Create and store **two** time-limited nonces for (a) system administrators' notification, and (b) user confirmation.
7. Send two email messages with links that include those nonces:

   * A **notification-only email message** to the current address, alerting the user to the impending change and providing a link to report unexpected activity.
   * A **confirmation-required email message** to the proposed new address, instructing the user to confirm the change and providing a link for unexpected situations.
8. Handle responses from the links accordingly.

### Recommended Process If the User DOES NOT HAVE Multifactor Authentication Enabled

1. Confirm the validity of the user's authentication cookie/token. If not valid, display a login screen.
2. Describe the process for changing the registered email address to the user.
3. Ask the user to submit a proposed new email address, ensuring it complies with system rules.
4. Request the user's current password for identity verification.
5. Store the proposed new email address as a pending change.
6. Create and store three time-limited nonces for system administrators' notification, user confirmation, and an additional step for password reliance.
7. Send two email messages with links to those nonces:

   * A **confirmation-required email message** to the current address, instructing the user to confirm the change and providing a link for an unexpected situation.
   * A **separate confirmation-required email message** to the proposed new address, instructing the user to confirm the change and providing a link for unexpected situations.
8. Handle responses from the links accordingly.

### Notes on the Above Processes

* It's worth noting that Google adopts a different approach with accounts secured only by a password -- [where the current email address receives a notification-only email](https://support.google.com/accounts/answer/55393?hl=en). This method carries risks and requires user vigilance.
* Regular social engineering training is crucial. System administrators and help desk staff should be trained to follow the prescribed process and recognize and respond to social engineering attacks. Refer to [CISA's "Avoiding Social Engineering and Phishing Attacks"](https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks) for guidance.

## Adaptive or Risk Based Authentication

A feature of more advanced applications is the ability to require different authentication stages depending on various environmental and contextual attributes (including but not limited to, the sensitivity of the data for which access is being requested, time of day, user location, IP address, or device fingerprint).

For example, an application may require MFA for the first login from a particular device but not for subsequent logins from that device. Alternatively, a single sign-on solution may authenticate the user and allow them to remain logged in for a day but require a reauthentication if they try to access their profile page.

Another option is the opposite approach where an application allows low risk access with just something that identifies the device (e.g., a specific mobile device fingerprint, a persistent cookie and browser fingerprint, etc. from the previous IP address) and then gradually requires stronger authentication for more sensitive operations. An example might be to allow someone to trigger something to see their current bank balance, but not the account number or anything else. If they need to see transactions, then the application puts them through some base level authentication and if they want to do any money movement, then MFA is required.

Questions that should be considered when implementing a mechanism like this include:

* Are the policies being put in place in line with any corporate policies and especially any regulatory policy?
* Which user‑ or device‑attributes (IP, geolocation, device fingerprint, time‑of‑day, behavioral biometrics, etc.) will we monitor at session start?
* Which of those signals need to be refreshed during an active session, and at what cadence?
* How will we ensure each signal’s accuracy and handle missing or low‑confidence data?
* What scoring model (weights, thresholds, ML, rule‑based, hybrid) will convert raw signals into a risk tier?
* Where will the model run (edge, API gateway, central service), and what is our latency budget?
* What action maps to each risk tier (allow, CAPTCHA, step‑up MFA, block, revoke session)?
* What user‑facing messages and error codes will accompany each action?
* At which exact code or platform layers will we invoke the risk engine (login controller, middleware, API gateway, service mesh)?
* How do we propagate decisions consistently across web, mobile, and API clients?
* How do we mutate, extend, or revoke tokens/cookies when a mid‑session risk check escalates?
* How do we synchronize state across multiple concurrent devices or browser tabs?
* What monitoring and alerting will be in place for potentially suspicious activity, including how the user is notified.

---

## Bibliography

1. [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
2. [Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
3. [REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
4. [OWASP Top Ten Web Application Security Risks](https://owasp.org/www-project-top-ten/)
5. [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)