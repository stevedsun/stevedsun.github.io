---
title: "Building A File Parser"
date: 2022-05-08T14:00:00+08:00
categories: [IoT Edge-Computing]
tags: [golang, fluentbit]
description: "Thinking in lexer for any format configuration file."
---

Last week, after reading this article - [How to Write a Lexer in Go](https://www.aaronraff.dev/blog/how-to-write-a-lexer-in-go), I found that it is not so difficult to design a configuration file parser by this article's mind-set. Then I tried to write a fluent-bit configuration parser, finally got this [Fluent-Bit configuration parser for Golang](https://github.com/stevedsun/go-fluentbit-conf-parser).

In this article, I want to introduce how to parse Fluent-bit configuration `.conf` file, and the thinking behind it.

## Fluent-bit configuration format and schema

```
[FIRST_SECTION]
    Key1  some value
    Key2  another value

[SECOND_SECTION]
    KeyN  3.14
```

Here is a classic mode configuration of Fluent-bit, it includes two parts:

- Section
- Key/value pair

First of all, we need to define a struct which represents the Fluent-bit configuration file.

```go
type FluentBitConf struct {
	Sections []Section
}

type Section struct {
	Name    string
	Entries []Entry
}

type Entry struct {
	Key   string
	Value interface{}
}
```

Once we have a struct, the next step is to parse tokens from the file and save their values into golang struct. We can copy the logic of the lexer to develop our fluentbit parser.

In a lexer program, the target characters which we want to parse out are called "Token", Token is also the keyword that our parser program is searching for. A parser program will read characters in a file one by one, whenever it found a token, the parser saves the value between tokens into the final structure and go ahead.

## Parse a single token

If we want to parse Section, we have to make the parser read characters one by one and stop at `[` character, which means the beginning of a Section. The parser must save the current state as `t_section` and keep parser reading until `]` character, the word between `[` and `]` is the Section value we need to persist into go struct.

```go

// define some tag to tell parser state
const (
	t_section = iota
)

func (parser *FluentBitConfParser) Parse() *FluentBitConf {
	var currSection *Section = nil

	for {
        // read charector one by one
		r, _, err := parser.reader.ReadRune()
		if err != nil {
            // stop at the end of file
			if err == io.EOF {
				if currSection != nil {
					parser.Conf.Sections = append(parser.Conf.Sections, *currSection)
				}
				return parser.Conf
			}
			return parser.Conf
		}
		switch r {
		case '\n':
			continue
		case '[':
			// save last config item
			if currSection != nil {
				parser.Conf.Sections = append(parser.Conf.Sections, *currSection)
			}
			// create new config item
			currSection = &Section{
				Name:    "",
				Entries: []Entry{},
			}
			parser.token = t_section
		default:
			if unicode.IsSpace(r) {
				continue
			}

            // here is important function, read the charectors after token-chareactor and save them into struct
			strValue, _ := parser.parseString()
			switch parser.token {
			case t_section:
				currSection.Name = strValue
				parser.token = t_entry_key
		}

	}
}
```

In function `parser.parseString()`, we have to read until the end of a value (for section, it's `]`), then return the value.

```go
func (parser *FluentBitConfParser) parseString() (string, error) {
	var val string = ""

	if err := parser.reader.UnreadRune(); err != nil {
		return "", err
	}
	for {
		r, _, err := parser.reader.ReadRune()
		if err != nil {
			if err == io.EOF {
				return val, nil
			}
			return "", err
		}

		if parser.token == t_section && r == ']' {
			return val, nil
		}

		val = val + string(r)
	}
}
```

That's all logic for parsing a section. To parse key/value pair is the same process, just note to make parser know which state it is and save values between whitespace or `\n`, you can see the code at [the github repo](https://github.com/stevedsun/go-fluentbit-conf-parser/blob/master/parser.go).

## Conclusion

To parse a configuration file, we have to

- Defining token (key characters)
- Reading characters and looking for a token
- Saving current state to tell parser which struct the following characters belong
