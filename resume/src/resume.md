# $title$ - $person.name$
## $person.title$

<span class="icon icon-id">[Contact](/contact)</span>

$if(summary.show)$
### $summary.title$

$summary.content$

$for(summary.category)$
- **$summary.category.title$:** $summary.category.content$
$endfor$
$endif$

### Experience

$for(experience)$
$if(experience.show)$
#### $experience.title$ <br> $experience.duration$ ($experience.date$) <br> $experience.company$ <br> $experience.location$
$if(experience.logo)$

![Logo $experience.company$]($experience.logo$)
$endif$

$experience.content$

$for(experience.description)$
- $experience.description$
$endfor$
$for(experience.category)$

**$experience.category.title$:** $experience.category.content$
$endfor$

$endif$
$endfor$

### Conference

$for(conference)$
$if(conference.show)$
#### [$conference.title$]($conference.link$) <br> $conference.duration$ ($conference.date$)
$if(conference.logo)$

![Logo $conference.title$]($conference.logo$)
$endif$

$conference.content$

$for(conference.description)$
- $conference.description$
$endfor$
$for(conference.category)$

**$conference.category.title$:** $conference.category.content$
$endfor$

$endif$
$endfor$

### Projects

$for(project)$
$if(project.show)$
#### [$project.title$ (&#9733;$project.star$)]($project.link$) <br> $project.duration$ ($project.date$)
$if(project.logo)$

![Logo $project.title$]($project.logo$)
$endif$

$project.content$
$for(project.category)$

**$project.category.title$:** $project.category.content$
$endfor$

$endif$
$endfor$

### Education

$for(education)$
$if(education.show)$
#### $education.title$ <br> $education.duration$ ($education.date$) <br> $education.location$
$if(education.logo)$

![Logo $education.title$]($education.logo$)
$endif$

$education.content$

$for(education.description)$
- $education.description$
$endfor$

$endif$
$endfor$

### Interests

$interest.content$

$for(interest.category)$
- **$interest.category.title$:** $interest.category.content$
$endfor$

