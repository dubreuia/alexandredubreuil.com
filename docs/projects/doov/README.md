# Domain Object Oriented Validation (dOOv)

<iframe src="https://ghbtns.com/github-btn.html?user=doov-io&repo=doov&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>

## Documentation

- [Website](https://doov.io)
- [Source code](https://github.com/doov-io/doov)
- [Conferences](https://dubreuia.github.io/alexandredubreuil.com/conferences/domain-object-oriented-validation-doov)

## Abstract

dOOv is a fluent API for typesafe domain model validation. It uses annotations, code generation and a type safe DSL to make domain model validation fast and easy.

Annotate your model with @Path annotations on field, qualifying them with field ids (see wiki section [Domain Model Annotation](https://github.com/doov-io/doov/wiki/Domain-Model-Annotation))

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

Use the dOOv code genrator to generate a DSL with elements `userFirstName`, `userLastName` and `userBirthDate` (see wiki section [DSL Code Generation](https://github.com/doov-io/doov/wiki/DSL-Code-Generation)). Then write your rules with entry point `DOOV#when` and terminal operation `ValidationRule#validate` (see wiki section [Validation Rules](https://github.com/doov-io/doov/wiki/Validation-Rules)).

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

You can then execute the rule on an instantiated model (see wiki section [Validation Engine](https://github.com/doov-io/doov/wiki/Validation-Engine)).

```java
// Execute the DSL on the model
DslModel model = new SampleModelWrapper(sampleModel);
Result result = rule.executeOn(model);
if (result.isFalse()) {
    // code for a result that doesn't validate
}
```

The result will return true or false depending on the result of the predicate, for example `Result#isTrue` means the predicate validated.

