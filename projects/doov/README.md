# Domain Object Oriented Validation (dOOv)

<iframe class="star" src="https://ghbtns.com/github-btn.html?user=doov-io&repo=doov&type=star&count=true" frameborder="0" scrolling="0"></iframe>

## Resources

<span class="icon icon-website">[Website](https://doov.io)</span> - <span class="icon icon-github">[Source Code](https://github.com/doov-io/doov)</span> - <span class="icon icon-link">[Conferences](https://dubreuia.github.io/alexandredubreuil.com/conferences/domain-object-oriented-validation-doov)</span>

## Abstract

![dOOv logo](doov-logo.png)

dOOv is a fluent API for typesafe domain model validation. It uses annotations, code generation and a type safe DSL to make domain model validation fast and easy.

Annotate your model with @Path annotations on field, qualifying them with field ids.

```java
public class User {

    @SamplePath(field = SampleFieldId.FIRST_NAME, readable = "user first name")
    private String firstName;

    @SamplePath(field = SampleFieldId.LAST_NAME, readable = "user last name")
    private String lastName;

    @SamplePath(field = SampleFieldId.BIRTHDATE, readable = "user birthdate")
    private LocalDate birthDate;

}
```

Use the dOOv code generator to generate a DSL with elements `userFirstName`, `userLastName` and `userBirthDate`. Then write your rules with entry point `DOOV#when` and terminal operation `ValidationRule#validate`.

```java
DOOV.when(userBirthdate().ageAt(today()).greaterOrEquals(18))
    .validate();
```

You can create more complex rules by chaining `and` and `or` or by using matching methods from the `DOOV` class like `matchAny`, etc.

```java
DOOV.when(userBirthdate().ageAt(today()).greaterOrEquals(18)
     .and(userFullName().isNotNull()))
    .validate()
```

You can then execute the rule on an instantiated model.

```java
// Execute the DSL on the model
DslModel model = new SampleModelWrapper(sampleModel);
Result result = rule.executeOn(model);
if (result.isFalse()) {
    // code for a result that doesn't validate
}
```

The result will return true or false depending on the result of the predicate, for example `Result#isTrue` means the predicate validated.

Once the predicate AST is instanciated, you can enjoy the commodities, including AST to text.

```java
System.out.println(rule.readable());
```

```bash
rule when 
    "user age" at today is greater than 18
        and "account email length" is lesser than "configuration max email size"
        and "account country" equals "french"
        and "account phone number" starts with "+33"
    validate
```

