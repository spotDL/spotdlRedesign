# Design Standards<a name="design-standards"></a>

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [The Deciding Factors (our design values)](#the-deciding-factors-our-design-values)
- [A few general notes](#a-few-general-notes)

<!-- mdformat-toc end -->

## The Deciding Factors (our design values)<a name="the-deciding-factors-our-design-values"></a>

- Simplicity:

  - What can we remove? Is this necessary to most (~80%+) of users?

  - Can we make it easier to use? Fewer steps?

- Focused Functionality:

  - spotDL is used to download "content" from Spotify. Does this help in doing that? (very narrow
    focus here people) A.K.A - is this a "need to have"?

  - If it's a "nice to have", will most of the users use it? (note: it's "most users
    **use**", not "most users **want**")

- Users first, provided its maintainable:

  - Will this do good to the users? They might have not even thought about it, it might
    make things more complex (more understanding of spotdl required to use it) but will it
    benefit the majority (~80%+) of them in the process?

  - Provided it helps the users, if it has a big impact on maintainability, it's still a
    no-no.

If a contribution satisfies at least 2 of our deciding values it gets accepted, else, it
doesn't.

## General Notes<a name="general-notes"></a>

1. The term 'users' is thrown around a lot. For a project like `FFmpeg`, users is that
   group of coders who are unafraid of a command-prompt (it says so on the downloads page
   itself). Here, '***users***' refers not to developers but normal *homo sapiens* - just
   about anybody who wants to download "content" from Spotify.

1. The term 'maintainability' has also been given significant weight. This is used in 2
   senses of the word:

   - General Simplicity - Can I read the code \***once** and understand what is going on?
   - Industry standard maintainability measures (the same one outlined on betterCodeHub)

1. The ideas outlined here are still very much a work in progress and is open to
   discussion, but we will stick to these. Some of the biggest companies & many more
   ambitious projects has all fallen to ruin because of the 'undisciplined pursuit of
   more'. That should not happen here. This is not so much of an outline of what we should
   do, rather an outline of what '**we should not do**'.

1. You're encouraged to question each contribution/existing functionality as required.
