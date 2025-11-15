#let title = [
  ZoteBoat - Software Architecture Document
]

#let group = [
  Group 324CC
]

#let members = [
  Lucas Ciucă, Ştefan Simion
]

#set page(
  paper: "a4",
  header: align(start)[#members #h(1fr) #group],
)

#set par(
  //first-line-indent: (amount: 1.2em, all: true),
  justify: true
)

#set text(
  font: "New Computer Modern Math",
  size: 12pt
)

#set heading(numbering: "1.")

#show link: underline

// Main Title
#pad(bottom: 1em,
  align(center, text(20pt)[
    *#title*
]))

= Introduction
#include "introduction.typ"
= System Overview
#include "overview.typ"
= Detailed Component Design
#include "components.typ"
= Deployment and Testing
#include "deployment_testing.typ"
= Conclusion
#include "conclusion.typ"
