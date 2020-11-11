from regos import Data_Entry, RegexGenerator


data = [{

            "string" : "I want to extract this id: 721 and this name: Damian",
            "selections" : [(27,29),(46,51)]

}]


generator = RegexGenerator()
generator.parse_selections(data)

for entry in generator.data_entries:
    print(entry)