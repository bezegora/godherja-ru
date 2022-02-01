# currently 5 formable bloodlines, Ragnarr bloodline, Karling bloodline, Matilda bloodline for beating excommunicated hre w/ special cb

########################################################################################################################################

Each bloodline has:
    - a trait applying the modifiers and dictating inheritance rules
    - a scripted gui. it is used to display the bloodline founder and extra inherit conditions if applicable
    - localization. in addition to the name and description, there are duplicates of the inheritance rules, they should match the trait. they are used in
      the gui and do not have an impact on the script
    - an extra_inherit scripted trigger. not strictly necessary if the bloodline has no extra conditions, but the error log will complain
    - an entry in the bloodline_effect_switch scripted effect block
    - an entry in the trait_counter script value
    - if the bloodline is historical a founder should be defined in the bloodline_set_founders on action
    - if the bloodline is formable, the bloodline_set_founder scripted effect should be used. Do not add the trait directly

##  Inhertiance Rules  ##

There are three primary rules controling inheritance:
    - inheritance type:
        - 'Matrilineal' bloodlines are passed only by the female line
        - 'Patrilineal' bloodlines are passed only by the male line
        - 'All' bloodlines are passed by both male and female lines
    - Matrilineal Override. Grants an exception to the above rules and allows men to pass matri bloodlines and women patri, if they are the dominant
      partner, or the only parent. Specifically men are considered dominant in regular marriage and concubinage, women are domiant in matrilineal 
      marriage and consortage. Both are considered dominant if they are the only defined parent, most often applicable in history.
    - Bastard Inheritance. controls if bastard children should inherit the bloodline

    - Extra Condition. A secondary set of conditions that the parent must meet to pass the bloodline. allows culture/religion specific bloodlines
      or anything else the trigger is written for. The test is performed on the parent, so different bloodlines can be passed on if a character 
      changes culture/faith during their life.

##  Vanilla Files Edited  ##

commmon:
    on_action
        child_birth_on_actions.txt - on_birth_bloodline on_action added to on_birth_child on 1 day delay
        game_start.txt - bloodline_set_founders on_action added on_game_start
events:
    interaction_events
        bastard_interaction_events.txt - trigger inherit_all_bloodlines effect in event bastard_interaction.0009
gui:
    window_character.gui - many changes. #BLOODLINE comment indicates them

##  Trait  ##

The bloodline trait uses flags to determine the inheritance rules and mark it as a bloodline.

there should always be a bloodline_<replace>_matri/_patri/_all flag to determine the inheritance type,
bloodline_<replace>_matri_override can be removed/commented to disable it 
bloodline_<replace>_allow_bastards can be removed/commented to disable it 
bloodline_<replace>_special_inheritance can be removed/commented to disable it 

the description in used in the gui to hide the bloodline in the character window traits and to show it in the bloodline list.

bloodline_<replace> = {
	index = 

	#modifiers

	flag = no_message
	flag = bloodline #marked as bloodline, for any_/every_bloodline_character
	flag = bloodline_<replace> #for specific bloodline

	# test for has_trait_with_flag = bloodline_$TRAIT$_matri/$TRAIT$_patri etc
	flag = bloodline_<replace>_matri #_matri/_patri/_all - inhertance
	flag = bloodline_<replace>_matri_override #allow inheritance for opposite marriages - mother will pass patri in matri marriage & father will pass matri in normal marriae
	flag = bloodline_<replace>_allow_bastards #do bastards inherits

	flag = bloodline_<replace>_special_inheritance #does the bloodline have extra inherit conditions?

	shown_in_ruler_designer = no
	shown_in_encyclopedia = no

	desc = { #The description is not shown. it is used to hide/show appropriately
		first_valid = {
			triggered_desc = {
				trigger = {
					NOT = { exists = this }
				}
				desc = bloodline_no
			}
			desc = bloodline_desc_blank
		}
	}
}

##  Scripted Gui  ##

The effect block is necessary as it is used to get the founder from a global variable as how to do so directly in localization
is not currently known. (pls tell me if you do figure it out)
The is_valid block is used to show the extra conditions in a tooltip, it can be removed if the bloodline has no extra conditions.

bloodline_<replace>_founder = {
	scope = character
	is_valid = { bloodline_<replace>_extra_inherit = yes }
	effect = {
		custom_description_no_bullet = {
			text = bloodline_founder
			subject = global_var:bloodline_<replace>_founder
		}
	}
}

##  Localization  ##

The bloodline name and description can be freely changed, the other localization keys correspond to the flags set in the trait and should match.
The gui expects  bloodline_<replace>_inherit to exist and have one of the values in the comments, the other keys are not strictly needed if they
are not defined as yes.

 trait_bloodline_<replace>:0 "Bloodline Name"
 bloodline_<replace>_inherit:0 "patri" # inheritance all, matri, patri
 bloodline_<replace>_matri_override:0 "yes" # does the bloodline pass in opposite dominant marriages, ie woman pass patri in matri marriage? yes/no
 bloodline_<replace>_bastards:0 "no" # do bastards inherit? yes/no
 bloodline_<replace>_special:0 "yes" # are there an extra conditions for inheritance? yes/no
 bloodline_<replace>_desc:0 "Bloodline description. try to keep below ~170 characters"