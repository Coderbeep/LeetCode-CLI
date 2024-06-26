# Leetcode CLI
Get your Leetcode account into the terminal. Search for problems, solve them and submit.

## Installation
#### Windows
```
pip install pyleetcode-cli
```

#### Linux
```
sudo pip install pyleetcode-cli
```

## Configuration
For this software to work you need to be logged into your Leetcode account. Your Leetcode `session_id` (can be found in cookies) is required for client initialization.
#### Chrome / Edge
``` chrome://settings/cookies/detail?site=leetcode.com ```
After you get your `session_id` you can either paste it into the right place in `config.yaml` file or use the CLI for the configuration:
``` 
leet config session_id YOUR_SESSION_ID
```

## Usage
```
Leet CLI

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Commands:
  {config,stats,list,problem,today,submission,submit,check}
    config              Configure the CLI
    stats               Display statistics
    list                Display problem list
    problem             Display problem
    today               Display today's problem.
    submission          Download submission code
    submit              Submit code answer
    check               Check code answer on example test
```

## Example workflow
You can search for the problem in multiple ways: using lists, fetching question of the day, random question or using specific ID.  

Take problem `1`, show its contents in the terminal and create a file with the code snippet:
```
leet problem 1 -fc
```

Now try to solve the problem. After that you can check the code against example test case:
```
leet test <filename>
```

Then try to submit the solution and wait for the response:
```
leet submit <filename>
```

## Screenshots
```
> leet stats
```

![](/images/stats.png)


```
> leet list 
```

![](/images/list.png)

```
> leet problem --contents
```
![](/images/today.png)

```
> leet submission 1 --show
```
![](/images/submission.png)

