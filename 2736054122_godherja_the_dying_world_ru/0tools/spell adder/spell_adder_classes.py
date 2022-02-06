from pathlib import Path
from datetime import datetime


class Settings:

    # adding settings requires an entry here and in the gui
    defaultsettings = {'confirm_save': True, 'shorten_paths': True} # NOTE: any iterables in the values should be immutable, as copy() below is shallow

    def __init__(self):
        try:
            with open('settings.txt', 'r') as settingsfile:
                lines = dePreAndSuffix(settingsfile.read()).splitlines()
                lines = filter(None, lines) # discard empty lines

                self.settings = {}
                for i in lines:
                    newgroup = (x.strip() for x in i.split('='))
                    self.settings[newgroup[0]] = newgroup[1]


                for i in defaultsettings:
                    try:
                        # will set the setting value to the same type as the default setting
                        # fails if it's not defined
                        settings[i] = type(defaultsettings[i])(settings[i]) 
                    except KeyError:
                        self.settings[i] = defaultsettings[i] # use default

        except FileNotFoundError:
            self.setDefault() # if there's no settings file, set the default

    def saveSettings(self):
        with open('settings.txt', 'w') as settingsfile:
            for i in self.settings:
                settingsfile.write(i + " = " + str(self.settings[i]) +'\n')

    def setDefault(self):
        self.settings = self.defaultsettings.copy()


def dePreAndSuffix(string: str, removing: str = '\n'):
    while string.startswith(removing):
        string = string[len(removing):]

    while string.endswith(removing):
        string = string[:-len(removing)]

    return string

def log(string: str):
    try:
        with open('log.txt', 'a') as file:
            file.write(string + '\n')
            
    except FileNotFoundError:
        with open('log.txt', 'x') as file:
            file.write(string + '\n')

def resetLog():
    with open('log.txt', 'w') as file:
        file.write('spell adder last opened on ' + datetime.now().strftime('%y-%m-%d %H: %M: %S') + '\n')


class Spell:

    spellType = 'base'

    def __init__(
                 self,
                 codename: str,
                 effect: str,
                 
                 name: str = None, # default is the above, with '_' made ' '.
                 desc: str = None,
                 
                 cost: str = "value = 0", # can be scripted

                 # valid_targets: set = ("self", "characters", "titles") # passing an empty set means the spell will show up but never be able to be cast
                 
                 is_shown_trigger = "",
                 trigger: str = "",
                 trigger_desc: str = None,
                 
                 ai_value_base = "100",
                 ai_value = ""
                ):
        
        self.codename = codename
        self.effect = effect
        if name != None:
            self.name = name
        if desc != None:
            self.desc = desc
        self.cost = cost
        
        self.is_shown_trigger = is_shown_trigger
        self.trigger = trigger
        if trigger_desc != None:
           self.trigger_desc = trigger_desc
           
        self.ai_value_base = ai_value_base
        self.ai_value = ai_value

    def _getPublicAttributes(self):
        attrs = dict()
        attrs['school'] = self.spellType # this shouldn't throw an atttrError
        for i in spellAttrNames:
            try:
                attrs[i] = getattr(self, i)
            except AttributeError:
                pass
        return attrs

    #def __eq__(self, other):
    #    try:
    #        return self._getPublicAttributes() == other._getPublicAttributes()
    #    except AttributeError:
    #        return False

    def __str__(self):
        return self.codename

    def getShortValues(self):
        return (
            self.codename,
            returnIfSet(self, 'name'),
            self.ai_value_base,
            self.spellType
        )
            


class spell_living(Spell):
    triggerignore = 'living_spell_trigger_generic = yes\n'

    spellType = 'living'


class spell_dead(Spell):
    triggerignore = 'dead_spell_trigger_generic = yes\n'

    spellType = 'dead'


class spell_mixed(Spell):
    triggerignore = 'mixed_spell_trigger_generic = yes\n'

    spellType = 'mixed'


class spell_other(Spell):
    triggerignore = 'other_spell_trigger_generic = yes\n'

    spellType = 'other'


class spell_generation(Spell):
    triggerignore = 'generation_spell_trigger_generic = yes\n'

    spellType = 'generation'


spellTypesDict = {i.spellType: i for i in (spell_living, spell_dead, spell_mixed, spell_other, spell_generation)}
spellAttrNames = {'codename', 'name', 'desc', 'effect', 'cost', 'is_shown_trigger', 'trigger', 'trigger_desc', 'ai_value_base', 'ai_value'} # this is a set
def genSpellObj(spellClass: str, values: dict):
    return spellTypesDict[spellClass](**values)


def returnIfPresent(dicti: dict, key: object):
    try:
        return dicti[key]
    except KeyError:
        log("key not found - " + key)
        return ""

def returnIfSet(obj: object, attribute: str, suppressErrorMessage: bool = False):
    try:
        return getattr(obj, attribute)
    except AttributeError:
        if not suppressErrorMessage:
            log("missing attribute: " + str(obj) + " does not have " + attribute)
        return ""

def ReadAndSplit(fileobj, splitstring: str = '\n}\n'):
    return fileobj.read().strip().split(splitstring)

def openPath(path, openMode: str = 'r'):
    return path.resolve().open(mode=openMode, encoding='utf-8-sig')

def splitKeyIfStringPresent(key: str, search: str, dictionary: dict = None, keyIsOneLine: bool = True):
    foundvar = key.find(search)
    if foundvar == -1:
        return False
    else:
        if dictionary != None:
            shortKey = key[:foundvar]
            if keyIsOneLine and '\n' in shortKey:
                print('shortKey:')
                print(shortKey)
                shortKey = shortKey[shortKey.rfind('\n') + len('\n'):]
                print(shortKey)
            dictionary[shortKey] = key[foundvar + len(search):] # this works because python is pass-by-reference
        return True

def tryGetValue(dictionary: dict, index: str):
    try:
        return dictionary[index]
    except KeyError:
        return None

def _stripLineBeginningString(string: str, toStrip: str):
    if string.startswith(toStrip):
        return string[len(toStrip):].replace('\n' + toStrip, '\n')
    else:
        return string.replace('\n' + toStrip, '\n')
        
class spellList:

    prefix = Path(__file__, type='safe') / '..' / '..' / '..' / 'common'
    scriptValuesFile = prefix / 'script_values' / 'gh_spell_cost_values.txt'
    scriptedEffectsFile = prefix / 'scripted_effects' / 'gh_spell_effects.txt'
    scriptedTriggersFile = prefix / 'scripted_triggers' / 'gh_spell_triggers.txt'
    scriptedGUIsFile = prefix / 'scripted_guis' / 'gh_sm_scripted_guis.txt'
    scriptedGUIeffectsFile = prefix / 'scripted_guis' / 'gh_spells.txt'
    aiSpellCastingFile = prefix / '..' / 'events' / 'godherja_events' / 'magic_events' / 'gh_ai_spell_event.txt'
    localizationFile = prefix / '..' / 'localization' / 'english' / 'godherja' / 'gh_spells_l_english.yml'

    def __init__(self):
        self.spells = self.loadSpells()
        self.spellsChanged = False
        self._codenamescache = set(i.codename for i in self.spells)

    def loadSpells(self):
        scriptValues = self.loadScriptValues()
        spells = set()
        scriptedShownTriggers, scriptedTriggers = self.loadScriptedTriggers()
        scriptedEffects = self.loadScriptedEffects()
        locNames, locDescs, locTriggerDescs = self.loadLocalization()
        AIvaluesBase, AIvalues = self.loadAIvalues()
        for i, spellClass in self.loadScriptedGUINames():

            print('loading key: ' + i)

            # only the optionals are defined here
            locName = tryGetValue(locNames, i)
            locDesc = tryGetValue(locDescs, i)
            locTrigger = tryGetValue(locTriggerDescs, i)
            
            spells.add(
                spellClass(
                    codename = i,
                    cost = returnIfPresent(scriptValues, i),
                    effect = returnIfPresent(scriptedEffects, i),
                    
                    is_shown_trigger = returnIfPresent(scriptedShownTriggers, i),
                    trigger = returnIfPresent(scriptedTriggers, i),
                    # valid_targets = ValidTargets[i],
                    
                    ai_value_base = returnIfPresent(AIvaluesBase, i),
                    ai_value = returnIfPresent(AIvalues, i),
                    
                    name = locName,
                    desc = locDesc,
                    trigger_desc = locTrigger
                )
            )

        return spells

    def deTabify(self, *tabbedDicts: dict, tabCount: int = 1):
        if len(tabbedDicts) == 1:
            return {key: _stripLineBeginningString(value, '\t' * tabCount) for key, value in tabbedDicts[0].items()}
        else:
            return tuple({key: _stripLineBeginningString(value, '\t' * tabCount) for key, value in currentDict.items()} for currentDict in tabbedDicts)
    
    def _loadFileGeneric(self, file, sepString: str = ' = {\n'):
        valuesDict = {}
        with openPath(file) as file:
            file = ReadAndSplit(file)
            for x in file:
                i = dePreAndSuffix(x).strip()
                # print("unseperated: " + i)
                if not splitKeyIfStringPresent(i, sepString, valuesDict):
                    print('no!')
                    print(sepString)
                    print(i)

        return self.deTabify(valuesDict)

    def loadScriptValues(self):
        return self._loadFileGeneric(self.scriptValuesFile, '_cost = {\n')

    def loadScriptedEffects(self):
        return self._loadFileGeneric(self.scriptedEffectsFile, '_effect = {\n')

    def loadScriptedTriggers(self):
        triggerDict = {}
        triggerShownDict = {}
        with openPath(self.scriptedTriggersFile) as file:
            file = ReadAndSplit(file)
            for i in file:
                # the following line depends on python's expression short-circuiting
                if not (splitKeyIfStringPresent(i, '_shown = {\n', triggerShownDict) or splitKeyIfStringPresent(i, '_trigger = {\n', triggerDict)):
                    print('no!')
                    print('trigger')
                    print(i)
                    

        return self.deTabify(triggerShownDict, triggerDict)

    def _loadScriptedGUIsection(self, section: str, classOfSpell: callable):
        spells = section.split("target = flag:")
        for i in spells[1:]:
            spellname = i[:i.find('\n')]
            if '#' in spellname:
                spellname = spellname[:spellname.find('#')].strip()
                
            # print('key:')
            # print(spellname)
            # print('\key')
            yield spellname, classOfSpell

    def loadScriptedGUINames(self):
        with openPath(self.scriptedGUIsFile) as file:
            fullfile = file.read()
            filenamesection = fullfile[:fullfile.find(
                """}
################
# SpellMenuFunc
# <-- collapse#######################################"""
                )]


            

            # living
            post1 = 0
            post2 = filenamesection.find(
                """
\t#####################################################
\t#				Dead Magic
\t# <-- collapse#######################################"""
                )
            for i, x in self._loadScriptedGUIsection(filenamesection[post1:post2], spell_living):
                # print("filename: " + filenamesection[post1:post2] + " /filename")
                yield i, x

            # dead
            post1 = post2
            post2 = filenamesection.find(
                """
\t#####################################################
\t#				Mixed Magic
\t# <-- collapse#######################################"""
                )
            for i, x in self._loadScriptedGUIsection(filenamesection[post1:post2], spell_dead):
                yield i, x

            # mixed
            post1 = post2
            post2 = filenamesection.find(
                """
\t#####################################################
\t#				Other Magic
\t# <-- collapse#######################################"""
                )
            for i, x in self._loadScriptedGUIsection(filenamesection[post1:post2], spell_mixed):
                yield i, x

            # other
            post1 = post2
            post2 = filenamesection.find(
                """
\t#####################################################
\t#				Generate Magic
\t# <-- collapse#######################################"""
                )
            for i, x in self._loadScriptedGUIsection(filenamesection[post1:post2], spell_other):
                yield i, x

            # generation
            post1 = post2
            post2 = filenamesection.find(
                """
\t\t}# root end dont erase
\t} #effect end dont erase
}"""
                )
            for i, x in self._loadScriptedGUIsection(filenamesection[post1:post2], spell_generation):
                yield i, x

    def loadLocalization(self):
        names = {}
        descs = {}
        trigger_descs = {}
        with openPath(self.localizationFile) as file:
            line = file.readline()
            while line:
                if '#' in line:
                    line = line[:line.find('#')]

                line = line.strip()

                if line and line != 'l_english:': # don't check empty lines, or the definition line
                    if '_desc_trigger:' in line:
                        val = line.find('"')
                        trigger_descs[line[:val - len('_desc_trigger:0 ')]] = line[val:].strip('"')
                    elif '_desc:' in line:
                        val = line.find('"')
                        descs[line[:val - len('_desc:0 ')]] = line[val:].strip('"')
                    else:
                        val = line.find('"')
                        names[line[:val - len('_name:0 ')]] = line[val:].strip('"')

                line = file.readline()
                        
                        
                
        return names, descs, trigger_descs
            

    def loadAIvalues(self):
        AIvaluesBase = {}
        AIvalues = {}
        with openPath(self.aiSpellCastingFile) as file:
            file = ReadAndSplit(file, '\toption = { # ')
            for i in file:
                name_end_index = i.find('\n')
                if name_end_index != -1:
                    myName = i[:name_end_index]

                    afterBase = i[i.find('base = ') + len('base = '):]
                    nextNewLine = afterBase.find('\n')
                    if '{' in i[:nextNewLine]: # multi-line script values exist
                        characterIndex = afterBase.find('{')
                        counter = 1
                        while counter > 1:
                            if afterBase[characterIndex] == '}':
                                counter -= 1
                            elif afterBase[characterIndex] == '{':
                                counter += 1
                            characterIndex += 1

                        nextNewLine = characterIndex + 1 # include the last bracket - the lost value is \n
                    AIvaluesBase[myName] = afterBase[:nextNewLine]

                    endOfValues = afterBase.find('\n\t\t}')
                    AIvalues[myName] = afterBase[nextNewLine + len('\n'):endOfValues]
                else:
                    print('no!')
                    print('ai')
                    print(i)

        return self.deTabify(AIvaluesBase, AIvalues, tabCount=2)

    def getSpells(self):
        return self.spells

    def getSpell(self, codename: str):
        for i in self.spells:
            if i.codename == codename:
                return i
        raise AttributeError

    def _refreshCodeNamesCache(self):
        self.spellsChanged = False
        self._codenamescache = set(i.codename for i in self.spells)
        return

    def getCodeNames(self):
        """should not be broken out of, as the cache will not be full"""
        if self.spellsChanged:
            self._refreshCodeNamesCache()

        return self._codenamescache

    def deleteSpell(self, spellObj: Spell):
        self.spellsChanged = True
        print('deleting spellObj :')
        print(spellObj)
        self.spells.remove(spellObj)
        return

    def addSpell(self, spellObj: Spell):
        self.spellsChanged = True
        self.spells.add(spellObj)
        return

    def editSpell(self, spellObj: Spell, entriesDict: dict, newSchool: str = None):
        if newSchool is None:
            newSchool = spellObj.spellType
        self.spellsChanged = True
        #print('\n\n\nunbased')
        #for i in self.spells:
        #    print(i)
        #print()
        self.deleteSpell(spellObj)
            
        self.addSpell(genSpellObj(newSchool, entriesDict))
        #print()
        #for i in self.spells:
        #    print(i)
        #print('b\nased\n\n\n')
        return


    def saveSpells(self, spellList: iter = None):
        if spellList == None:
            spellList = self.spells

        names, descs, trigger_descs = self.loadLocalization()
        with openPath(self.scriptedGUIsFile, 'w') as guiFile, \
             openPath(self.scriptedGUIeffectsFile, 'w') as guiEffectsFile, \
             openPath(self.scriptValuesFile, 'w') as valuesFile, \
             openPath(self.scriptedEffectsFile, 'w') as effectsFile, \
             openPath(self.scriptedTriggersFile, 'w') as triggersFile, \
             openPath(self.aiSpellCastingFile, 'w') as aiFile:
             #openPath(self.localizationFile, 'w') as locFile: # this file is additive, so if a spell is deleted the name stays. This is not the case if an existing spell's name is removed.

            locFile.write('l_english:\n ')

            self._preSaveToAI(aiFile)
            self._saveToGUI(guiFile, spellList)
            self._preSaveToGUI(guiEffectsFile)
            
            # maybe add datetime change logging here?
            for i in spellList:
                self._saveToIndividual(valuesFile, i.codename, i.cost, '_cost')
                self._saveToIndividual(effectsFile, i.codename, i.effect, '_effect')
                self._saveToIndividual(triggersFile, i.codename, i.is_shown_trigger, '_shown')
                self._saveToIndividual(triggersFile, i.codename, i.trigger, '_trigger')
                self._saveToAI(aiFile, i.codename, i.ai_value_base, i.ai_value)
                
                self._saveToIndividual(guiEffectsFile, i.codename,
                                       "scope = character\n" + "effect = {\n" + '\t' + i.codename + "_effect = yes\n" + '}',
                                       '')

                #try:
                #    names[i.codename] = i.name
                #except AttributeError:
                #    names.pop(i.codename, None)
                #try:
                #    descs[i.codename] = i.desc
                #except AttributeError:
                #    descs.pop(i.codename, None)
                #try:
                #    trigger_descs[i.codename] = i.trigger_desc
                #except AttributeError:
                #    trigger_descs.pop(i.codename, None)

            #for key, value in names.items():
            #    print(key)
            #    locFile.write('\n ')
            #    locFile.write(key + '_name:0 "' + value + '"\n ')
            #    
            #    descValue = descs.pop(key, None)
            #    if descValue is not None:
            #        locFile.write(key + '_desc:0 "' + descValue + '"\n ')

             #   triggerValue = trigger_descs.pop(key, None)
             #   if triggerValue is not None:
             #       locFile.write(key + '_desc_trigger:0 "' + triggerValue + '"\n ')

            #for key, value in descs.items():
            #    locFile.write('\n ')
            #    locFile.write(key + ':0 "' + value + '"\n ')
            #    
             #   triggerValue = trigger_descs.pop(key, None)
              #  if triggerValue is not None:
               #     locFile.write(key + '_desc_trigger:0 "' + triggerValue + '"\n ')
#
           # for key, value in trigger_descs.items():
           #     locFile.write('\n ')
            #    locFile.write(key + ':0 "' + value + '"\n ')


            self._postSaveToAI(aiFile)

        return

    def _saveToIndividual(self, file, name: str, cost: str = 'value = 0', suffix: str = ''):
        #print(cost)
        cost = '\t' + cost.replace('\n', '\n\t') # tabification
        #print(cost)
        file.write(name + suffix + ' = {\n' + cost + '\n}\n\n')
        return

    def _preSaveToAI(self, file: object):
        """ writes the event and the no spell option"""
        file.write("""namespace = magic_ai

magic_ai.9999 = { # ai check spells
	hidden = yes

	trigger = {
		has_variable = magic_counter
		is_ai = yes
	}

	immediate = {
		save_scope_value_as = {
			name = more_spells
			value = yes
		}
	}

	after = {
		if = {
			limit = { scope:more_spells = yes }
			trigger_event = magic.9999
		}
	}

	option = { # none
		trigger = {}

		save_scope_value_as = {
			name = more_spells
			value = no
		}

		ai_value = {
			base = 100
		}
	}""")
        return

    def _saveToAI(self, file: object, codename: str, base: str, mods: str):
        newlinesandtabs = '\n\t\t\t'
        base = dePreAndSuffix(base)
        codename = dePreAndSuffix(codename)
        file.write('\n\n\toption = { # ' + codename)
        file.write('\n\n\t\t' + 'ai_chance = {')
        
        writingstring = '\n' + 'base = ' + (base if base else '0') + '\n\n' + mods
        file.write(writingstring.replace('\n', newlinesandtabs)) # indentation
        file.write('\n\t\t}')
        file.write('\n\t\t' + codename + '_effect = yes')
        file.write('\n\t\t' + 'trigger = {')
        file.write('\n\t\t\t' + codename + '_shown = yes')
        file.write('\n\t\t\t' + codename + '_trigger = yes')
        file.write('\n\t\t}')
        file.write('\n\t}')
        return

    def _postSaveToAI(self, file):
        file.write('\n}')
        return

    def _saveToGUI(self, file, savingSpells):
        spellsByType = spellTypesDict.copy()
        for key in spellsByType:
            spellsByType[key] = tuple(filter(lambda x: x.spellType == key, savingSpells))
        # the above sorts the spells by type, e.g. {'living': set(<spell1>, <spell2>), ...

        file.write("""###########################
# Spell Menu By CASTOX (warning: deleting comments or otherwise manually editing the file may screw with the Python program. Please use that instead. Of course, edit if you wish, but be prepared for Panzer's wrath if it breaks)
##################
# Get Spell Lists 
##################
get_spell_list = {
	scope = character
	effect = {
		root = {""")

        for magicType in spellsByType:
            file.write("""
	#####################################################
	#				""" + magicType + """ Magic
	# <-- collapse#######################################""")

            for spell in spellsByType[magicType]:
                file.write("""
			add_to_variable_list = {
				name = list_""" + magicType + """_magic
				target = flag:""" + spell.codename + """
			}""")

        file.write("""
		}# root end dont erase
	} #effect end dont erase
}
################
# SpellMenuFunc
# <-- collapse#######################################

	set_spell_to_cast = {
		scope = character
		
		effect = {
			root = {
				every_in_list = {
					variable = lands_realm
					remove_variable = is_selected
				}
			}
		}
	}
	realm_char = {
		scope = character
		effect = {
			root = {
				every_vassal = {
					limit = {
						NOT = {
							is_imprisoned = yes
						}
					}
					root = {
						add_to_variable_list = {
							name = character_in_realm
							target = prev
						}
					}
				}
			}
		}
	}

	enemy_char = {
		scope = character
		effect = {
			every_war_enemy = {
				limit = {
					is_at_war_with = prev
					NOT = {
						is_player_selected = no
					}
				}
				root = {
					add_to_variable_list = {
						name = enemy_in_realm
						target = prev
					}
				}
			}		
		}
	}

	prisoner_char = {
		scope = character
		effect = {
			root = {
				every_prisoner = {
					limit = {
						is_imprisoned_by = prev
						is_alive = yes
					}
					root = {
						add_to_variable_list = {
							name = prisoner_in_realm
							target = prev
						}
					}
				}
			}
		}
	}
	realm_lands = {
        scope = character
        effect = {
            root = {
                every_held_title = {
                	limit = {
                		NOT = {
                			tier = tier_barony
                			tier = tier_duchy
                			tier = tier_kingdom
                			tier = tier_empire
                		}
                	}
                    root = {
                    	add_to_variable_list = {
                        	name = lands_realm
                        	target = prev
                    	}
                	}
            	}
        	}
    	}
    }

    enemy_realm_lands = {
    	scope = character
    	effect = {
    		every_war_enemy = {
    			limit = {
    				is_at_war_with = prev
    			}
    			every_sub_realm_county = {
    				root = {
    					add_to_variable_list = {
    						name = enemy_lands
    						target = prev
    					}
    				}
    			}
    		}
    	}
    }

	title_selected = {
		scope = character

		saved_scope = {
			target
		}
		effect = {
			if = {
				limit = {
					is_target_in_variable_list = { name = spell_l_targets target = scope:target }
				}
				remove_list_variable = { name = spell_l_targets target = scope:target }
				clear_variable_list = spell_l_targets
			}
			else_if = {
				clear_variable_list = spell_l_targets
				add_to_variable_list = {
					name = spell_l_targets
					target = scope:target
				}
			}
			root = {
				every_in_list = {
					variable = character_in_realm
					remove_variable = is_selected
				}
				clear_variable_list = spell_targets
			}
		}
	}
	title_select = {

		scope = title
		effect = {

			root = {
				clear_selected_char = {}
			}

			if = {
				limit ={
					has_variable = is_selected
				}
		
				remove_variable = is_selected
			}
			else = {
				set_variable = {
					name = is_selected
					value = flag:selected
				}
			}
		}
	}
	char_selected = {
		scope = character

		saved_scope = {
		target
		}
		effect = {
			if = {
				limit = {
					is_target_in_variable_list = { name = spell_targets target = scope:target }
				}
				remove_list_variable = { name = spell_targets target = scope:target }
				clear_variable_list = spell_targets
			}
			else_if = {
				clear_variable_list = spell_targets
				add_to_variable_list = {
					name = spell_targets
					target = scope:target
				}
			}
			root = {
				every_in_list = {
					variable = lands_realm
					remove_variable = is_selected
				}
				clear_variable_list = spell_l_targets
			}

		}
	}
	char_select = {
		scope = character
		effect = {
			if = {
				limit ={
					has_variable = is_selected
				}
		
				remove_variable = is_selected
			}
			else = {
				set_variable = {
					name = is_selected
					value = flag:selected
				}
			}
		}
	}

########################
# Spells for CHECKS
# <-- collapse#######################################
""")

        print('\n\nNO!!!!!\n')
        print(spellsByType)
        print()
        for magicType in spellsByType:
            file.write("\n\n\t#" + magicType)
            print(spellsByType[magicType])

            for spell in spellsByType[magicType]:
                print(spell)
                currentName = spell.codename
                startLine = '\n' + currentName + '_check = {'

                mainlines = (
                    'scope = character',
                    'is_shown = {',
                    '\t' + currentName + '_shown = yes',
                    '}',
                    '',
                    'is_valid = {',
                    '\t' + currentName + '_trigger = yes',
                    '}'
                    )

                mainlinestext = '\n\t' + '\n\t'.join(mainlines)

                endLines = '\n}'

                maintext = startLine + mainlinestext + endLines
                file.write(maintext.replace('\n', '\n\t\t') + '\n')

        file.write('\n\n# THE END')
        return

    def _preSaveToGUI(self, file: object):
        file.write("""
####SPELL EFFECTS

### LIVING MAGIC ###

## ETERNAL LIFE, ENDLESS TORTURE ## thank you doodle
""")
        return
