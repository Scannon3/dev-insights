What problem does a virtual environment solve, and what goes wrong without one?
-a virtual environment isolates a project. This way everything we need exists inside our project folder in a virtual environment. This way everything that's needed for requirements will always be true.
Why do teams use branches instead of committing directly to main?
-main is production code, so making branches makes things like testing and reverting much easier.
What is a type hint, and what class of bugs does it help catch before you run the code?
- it lets you know what type the function expects. it will help catch the type of bugs where a type is read that wasnt expected, like string to int.
Give an example of code an AI might generate that runs fine but is still wrong or unsafe. How would you catch it?
- an auth method that allows more than it should. Catch through testing.
What does "I own this code" mean if an AI wrote most of it?
- it means that i understand why the code is there, what it does, and what would happen if it was removed.