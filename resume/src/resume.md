# $title$ - $person.name$ <br> $person.title$

$if(summary.show)$
## $summary.title$

$summary.content$

$for(summary.category)$
- **$summary.category.title$:** $summary.category.content$
$endfor$
$endif$

## Experience

$for(experience)$
$if(experience.show)$
### $experience.title$ <br> $experience.duration$ ($experience.date$) <br> $experience.company$ <br> $experience.location$

$experience.content$

$for(experience.description)$
- $experience.description$
$endfor$
$for(experience.category)$

**$experience.category.title$:** $experience.category.content$
$endfor$

$endif$
$endfor$

## Conference

$for(conference)$
$if(conference.show)$
### $conference.title$ <br> $conference.duration$ ($conference.date$)

$conference.content$

$for(conference.description)$
- $conference.description$
$endfor$
$for(conference.category)$

**$conference.category.title$:** $conference.category.content$
$endfor$

$endif$
$endfor$

## Projects

$for(project)$
$if(project.show)$
### $project.title$ <br> $project.duration$ ($project.date$)

$project.content$
$for(project.category)$

**$project.category.title$:** $project.category.content$
$endfor$

$endif$
$endfor$

## Education

$for(education)$
$if(education.show)$
### $education.title$ <br> $education.duration$ ($education.date$) <br> $education.location$

$education.content$

$for(education.description)$
- $education.description$
$endfor$

$endif$
$endfor$

## Interests

$interest.content$

$for(interest.category)$
- **$interest.category.title$:** $interest.category.content$
$endfor$

