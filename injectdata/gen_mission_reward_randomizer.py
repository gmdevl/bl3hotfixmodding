#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

from bl3hotfixmod.bl3hotfixmod import Mod, BVC, BVCF, Pool

mod = Mod('mission_reward_randomizer.txt',
        'Mission Reward Randomizer',
        [
            "Randomizes the rewards given by missions.  Reward types should remain",
            "constant -- if it originally gives a pistol, you should get a legendary",
            "pistol of some sort.  This does not include customization rewards.",
            "",
            "More or less intended to be used alongside my Expanded Legendary Pools",
            "mods, for the most interesting rewards.",
            "",
            "Relatively untested!  It's quite possible that some missions were missed.",
            "The data here was programmatically generated from JohnWickParse data",
            "serializations, and JWP has problems with some objects.",
        ],
        'MissRwdRando',
        )

# There are various ways to accomplish this, and of course I go for a
# super over-engineered method.  Ah, well!

(AR, HW, PS, SG, SM, SR, SH, GM, CM, AF, SK, HD, TK, RD) = range(14)
type_blacklist = {SK, HD, TK, RD}

leg_pools = {
        AR: '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary',
        HW: '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary',
        PS: '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary',
        SG: '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary',
        SM: '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary',
        SR: '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary',
        SH: '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary',
        GM: '/Game/GameData/Loot/ItemPools/GrenadeMods/ItemPool_GrenadeMods_05_Legendary',
        CM: '/Game/Gear/ClassMods/_Design/ItemPools/ItemPool_ClassMods_05_Legendary',
        AF: '/Game/Gear/Artifacts/_Design/ItemPools/ItemPool_Artifacts_05_Legendary',

        # If we were going to randomize customizations (as we were doing for awhile), we'd use
        # these.  These types are now blacklisted, though.
        SK: '/Game/Pickups/Customizations/_Design/ItemPools/Skins/ItemPool_Customizations_Skins_Loot',
        HD: '/Game/Pickups/Customizations/_Design/ItemPools/Heads/ItemPool_Customizations_Heads_Loot',
        TK: '/Game/Gear/WeaponTrinkets/_Design/ItemPools/ItemPool_Customizations_WeaponTrinkets_Loot',
        RD: '/Game/Pickups/Customizations/_Design/ItemPools/PlayerRoomDeco/ItemPool_Customizations_RoomDeco_Loot',
        }
for drop_type in leg_pools.keys():
    leg_pools[drop_type] = Mod.get_full_cond(leg_pools[drop_type], 'ItemPoolData')

for (mission_obj, drop_type) in [
        # This list generated by mission_rewards.py in my bl3data dir
        # Would be nice to have mission names in here, but the JWP serializations we rely on
        # for the data doesn't manage to serialize the name
        ('/Game/Missions/Plot/Mission_Ep01_ChildrenOfTheVault.Default__Mission_Ep01_ChildrenOfTheVault_C:RewardData_OakMissionRewardData', GM),
        ('/Game/Missions/Plot/Mission_Ep02_Sacrifice.Default__Mission_Ep02_Sacrifice_C:RewardData_OakMissionRewardData', SK),
        ('/Game/Missions/Plot/Mission_Ep03_GetVaultMap.Default__Mission_Ep03_GetVaultMap_C:RewardData_OakMissionRewardData', HD),
        ('/Game/Missions/Plot/Mission_Ep04_EarnSpaceship.Default__Mission_Ep04_EarnSpaceship_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Plot/Mission_Ep05_Sanctuary.Default__Mission_Ep05_Sanctuary_C:RewardData_OakMissionRewardData', SH),
        ('/Game/Missions/Plot/Mission_Ep06_MeetMaya.Default__Mission_Ep06_MeetMaya_C:RewardData_OakMissionRewardData', SM),
        ('/Game/Missions/Plot/Mission_Ep08_OrbitalPlatform.Default__Mission_Ep08_OrbitalPlatform_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Plot/MIssion_Ep09_AtlasHQ.Default__MIssion_Ep09_AtlasHQ_C:RewardData_OakMissionRewardData', HD),
        ('/Game/Missions/Plot/Mission_Ep10_CityVault.Default__Mission_Ep10_CityVault_C:RewardData_OakMissionRewardData', TK),
        ('/Game/Missions/Plot/Mission_Ep11_PrisonBreak.Default__Mission_Ep11_PrisonBreak_C:RewardData_OakMissionRewardData', SR),
        ('/Game/Missions/Plot/Mission_Ep12_GrandTour.Default__Mission_Ep12_GrandTour_C:RewardData_OakMissionRewardData', GM),
        ('/Game/Missions/Plot/Mission_Ep13_JakobsRebellion.Default__Mission_Ep13_JakobsRebellion_C:RewardData_OakMissionRewardData', HD),
        ('/Game/Missions/Plot/Mission_Ep13_Watership.Default__Mission_Ep13_Watership_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Plot/Mission_Ep15_MarshFields.Default__Mission_Ep15_MarshFields_C:RewardData_OakMissionRewardData', AR),
        ('/Game/Missions/Plot/Mission_Ep16_DesertVault.Default__Mission_Ep16_DesertVault_C:RewardData_OakMissionRewardData', HD),
        ('/Game/Missions/Plot/Mission_Ep16_SiblingRivalry.Default__Mission_Ep16_SiblingRivalry_C:RewardData_OakMissionRewardData', SK),
        ('/Game/Missions/Plot/Mission_Ep17_BigChase.Default__Mission_Ep17_BigChase_C:RewardData_OakMissionRewardData', AF),
        ('/Game/Missions/Plot/Mission_Ep19_MinerDetails.Default__Mission_Ep19_MinerDetails_C:RewardData_OakMissionRewardData', SH),
        ('/Game/Missions/Plot/Mission_Ep20_FirstVaultHunter.Default__Mission_Ep20_FirstVaultHunter_C:RewardData_OakMissionRewardData', SK),
        ('/Game/Missions/Side/Zone_0/Prologue/Mission_FineDining.Default__Mission_FineDining_C:RewardData_OakMissionRewardData', SM),
        ('/Game/Missions/Side/Zone_0/Prologue/Mission_VendingMachineRepair.Default__Mission_VendingMachineRepair_C:RewardData_OakMissionRewardData', HD),
        ('/Game/Missions/Side/Zone_0/Sacrifice/Mission_GoldenCalves.Default__Mission_GoldenCalves_C:RewardData_OakMissionRewardData', SH),
        ('/Game/Missions/Side/Zone_0/Sacrifice/Mission_HeadCase.Default__Mission_HeadCase_C:RewardData_OakMissionRewardData', SR),
        ('/Game/Missions/Side/Zone_1/Athenas/Mission_MonkMission.Default__Mission_MonkMission_C:RewardData_OakMissionRewardData', SH),
        ('/Game/Missions/Side/Zone_1/AtlasHQ/Mission_RatchetItUp.Default__Mission_RatchetItUp_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Side/Zone_1/City/Mission_DynastyDiner.Default__Mission_DynastyDiner_C:RewardData_OakMissionRewardData', HW),
        ('/Game/Missions/Side/Zone_1/City/Mission_RiseAndGrind.Default__Mission_RiseAndGrind_C:RewardData_OakMissionRewardData', SH),
        ('/Game/Missions/Side/Zone_1/City/Mission_WizardOfNogs.Default__Mission_WizardOfNogs_C:RewardData_OakMissionRewardData', GM),
        ('/Game/Missions/Side/Zone_1/City/Mission_WizardOfNogs.OBJ_MissionRewardSkin_Objective:OakMissionRewardData_5', HD),
        ('/Game/Missions/Side/Zone_1/OrbitalPlatform/OppositionResearch/Mission_OppResearch.Default__Mission_OppResearch_C:RewardData_OakMissionRewardData', TK),
        ('/Game/Missions/Side/Zone_1/Towers/Mission_KillKillavolt.Default__Mission_KillKillavolt_C:RewardData_OakMissionRewardData', RD),
        ('/Game/Missions/Side/Zone_1/Towers/Mission_LastKatagawa.Default__Mission_LastKatagawa_C:RewardData_OakMissionRewardData', SR),
        ('/Game/Missions/Side/Zone_1/Towers/Mission_Porta-Prison.Default__Mission_Porta-Prison_C:RewardData_OakMissionRewardData', HW),
        ('/Game/Missions/Side/Zone_2/Mansion/Mission_WitchesBrew.Default__Mission_WitchesBrew_C:RewardData_OakMissionRewardData', GM),
        ('/Game/Missions/Side/Zone_2/Prison/Mission_FreeHugs.OBJ_SideWithGangLeader_Objective:OakMissionRewardData_8', SG),
        ('/Game/Missions/Side/Zone_2/Prison/Mission_FreeHugs.OBJ_TalkwithHugs_Objective:OakMissionRewardData_8', SH),
        ('/Game/Missions/Side/Zone_2/Prison/Mission_MalevolentPractice.Default__Mission_MalevolentPractice_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Side/Zone_2/Wetlands/Mission_DudeBro.Default__Mission_DudeBro_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Side/Zone_2/Wetlands/Mission_TortureTruck.Default__Mission_TortureTruck_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Side/Zone_3/Desert/Mission_BabyDancer.Default__Mission_BabyDancer_C:RewardData_OakMissionRewardData', SM),
        ('/Game/Missions/Side/Zone_3/Desert/Mission_BirthdaySurprise.Default__Mission_BirthdaySurprise_C:RewardData_OakMissionRewardData', PS),
        ('/Game/Missions/Side/Zone_3/Desert/Mission_EchoNetNeutrality.Default__Mission_EchoNetNeutrality_C:RewardData_OakMissionRewardData', SR),
        ('/Game/Missions/Side/Zone_3/Desert/Mission_ItsComplicated.Default__Mission_ItsComplicated_C:RewardData_OakMissionRewardData', TK),
        ('/Game/Missions/Side/Zone_3/Mine/Mission_BridgeInTheDark.Default__Mission_BridgeInTheDark_C:RewardData_OakMissionRewardData', SG),
        ('/Game/Missions/Side/Zone_3/Mine/Mission_GrowingPains.Default__Mission_GrowingPains_C:RewardData_OakMissionRewardData', SH),
        ('/Game/Missions/Side/Zone_3/Mine/Mission_WildlifeConservation.Default__Mission_WildlifeConservation_C:RewardData_OakMissionRewardData', SR),
        ('/Game/Missions/Side/Zone_3/Motorcade/Mission_Gameshow.Default__Mission_Gameshow_C:RewardData_OakMissionRewardData', TK),
        ('/Game/Missions/Side/Zone_3/Motorcade/Mission_Homestead_Part3.Default__Mission_Homestead_Part3_C:RewardData_OakMissionRewardData', AR),
        ('/Game/Missions/Side/Zone_3/Motorcade/Mission_Just_Desserts.Default__Mission_Just_Desserts_C:RewardData_OakMissionRewardData', GM),
        ('/Game/Missions/Side/Zone_4/Desolate/Mission_Canonization.Default__Mission_Canonization_C:RewardData_OakMissionRewardData', SM),
        ('/Game/Missions/Side/Zone_4/Desolate/Mission_DestroyerOfWorlds.Default__Mission_DestroyerOfWorlds_C:RewardData_OakMissionRewardData', SR),
        ('/Game/Missions/Side/Zone_4/Desolate/Mission_Homeopathological.Default__Mission_Homeopathological_C:RewardData_OakMissionRewardData', AR),
        ('/Game/Missions/Side/Zone_4/Desolate/Mission_ItsAlive2.Default__Mission_ItsAlive2_C:RewardData_OakMissionRewardData', SH),
        ('/Game/PatchDLC/Dandelion/Missions/Plot/Mission_DLC1_Ep02_MeetCrad.Default__Mission_DLC1_Ep02_MeetCrad_C:RewardData_OakMissionRewardData', SH),
        ('/Game/PatchDLC/Dandelion/Missions/Plot/Mission_DLC1_Ep03_Impound.Default__Mission_DLC1_Ep03_Impound_C:RewardData_OakMissionRewardData', GM),
        ('/Game/PatchDLC/Dandelion/Missions/Plot/Mission_DLC1_Ep04_Trashtown.Default__Mission_DLC1_Ep04_Trashtown_C:RewardData_OakMissionRewardData', AR),
        ('/Game/PatchDLC/Dandelion/Missions/Plot/Mission_DLC1_Ep05_ThePlan.Default__Mission_DLC1_Ep05_ThePlan_C:RewardData_OakMissionRewardData', PS),
        ('/Game/PatchDLC/Dandelion/Missions/Plot/Mission_DLC1_Ep07_TheHeist.Default__Mission_DLC1_Ep07_TheHeist_C:RewardData_OakMissionRewardData', SH),
        ('/Game/PatchDLC/Dandelion/Missions/Side/Mission_DLC1_Side_AcidTrip.Default__Mission_DLC1_Side_AcidTrip_C:RewardData_OakMissionRewardData', SG),
        ('/Game/PatchDLC/Dandelion/Missions/Side/Mission_DLC1_Side_DoItForDigby_Part3.Default__Mission_DLC1_Side_DoItForDigby_Part3_C:RewardData_OakMissionRewardData', AR),
        ('/Game/PatchDLC/Dandelion/Missions/Side/Mission_DLC1_Side_DoubleDown.Default__Mission_DLC1_Side_DoubleDown_C:RewardData_OakMissionRewardData', SH),
        ('/Game/PatchDLC/Dandelion/Missions/Side/Mission_DLC1_Side_GreatEscape.Default__Mission_DLC1_Side_GreatEscape_C:RewardData_OakMissionRewardData', AR),
        ('/Game/PatchDLC/Dandelion/Missions/Side/Mission_DLC1_Side_RegainingOnesFeet.Default__Mission_DLC1_Side_RegainingOnesFeet_C:RewardData_OakMissionRewardData', SH),
        ('/Game/PatchDLC/Hibiscus/Missions/Plot/EP02_DLC2.Default__EP02_DLC2_C:RewardData_OakMissionRewardData', SG),
        ('/Game/PatchDLC/Hibiscus/Missions/Plot/EP06_DLC2.Default__EP06_DLC2_C:RewardData_OakMissionRewardData', PS),
        ('/Game/PatchDLC/Hibiscus/Missions/Side/SideMission_DLC2_HappilyEverAfter.Default__SideMission_DLC2_HappilyEverAfter_C:RewardData_OakMissionRewardData', SG),
        ('/Game/PatchDLC/Hibiscus/Missions/Side/SideMission_DLC2_PrivateEyePart3.Default__SideMission_DLC2_PrivateEyePart3_C:RewardData_OakMissionRewardData', PS),
        ('/Game/PatchDLC/Hibiscus/Missions/Side/SideMission_DLC2_WeSlassPart3.Default__SideMission_DLC2_WeSlassPart3_C:RewardData_OakMissionRewardData', SG),
        ]:

    if drop_type not in type_blacklist:
        mod.reg_hotfix(Mod.PATCH, '',
                mission_obj,
                'ItemPoolReward',
                leg_pools[drop_type])

mod.close()
