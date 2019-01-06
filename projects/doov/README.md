# Domain Object Oriented Validation (dOOv)

<iframe class="star" src="https://ghbtns.com/github-btn.html?user=doov-io&repo=doov&type=star&count=true" frameborder="0" scrolling="0"></iframe>

## Resources

- [Website](https://doov.io)
- [Source code](https://github.com/doov-io/doov)
- [Conferences](https://dubreuia.github.io/alexandredubreuil.com/conferences/domain-object-oriented-validation-doov)

## [Conference slides](https://alexandredubreuil.com/conferences/domain-object-oriented-validation-doov/dsl_to_go_beyond_bean_validation_openrday.html)

<iframe class="slides" src="https://alexandredubreuil.com/conferences/domain-object-oriented-validation-doov/dsl_to_go_beyond_bean_validation_openrday.html" frameborder="0"></iframe>

## [Conference video](https://www.youtube-nocookie.com/embed/a0PJ3NuSA_c)

<iframe class="video" src="https://www.youtube-nocookie.com/embed/a0PJ3NuSA_c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

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

