#Imports
import random

#Start the HTML File
to_html = ["<!DOCTYPE html>","<html>","<head>","<link rel='stylesheet' href='obfuscation.css'/>",
           "<title>","Testing CCP","</title>","</head>"]

#Produce a random letter between each real letter function
def obfuscate_function(text,tag):
    for letter in text:
        to_html.append(''.join(['<',tag,' class="letter"','>',letter,'</',tag,'>']))
        to_html.append(''.join(['<',tag,' class="character"','>',chr(random.randint(ord('a'), ord('z'))),'</',tag,'>']))

#What you want the heading to be
#heading = "Testing: Colored Conventions Project"

#What you want the body to be
body = """
CONSTITUTION
OF THE

AMERICAN SOCIETY

OF FREE PERSONS OF COLOUR,

FOR IMPROVING THEIR CONDITION IN THE UNITED STATES; FOR PURCHASING LANDS; AND FOR THE ESTABLISHMENT OF A SETTLEMENT IN UPPER CANADA,

ALSO

THE PROCEEDINGS OF THE CONVENTION,

WITH THEIR

ADDRESS

TO

THE FREE PERSONS OF COLOUR

IN THE

UNITED STATES.


PHILADELPHIA:

PRINTED BY J.W. ALLEN, NO 26, STRAWBERRY-ST.

1831.

MINUTES OF THE CONVENTION.

AT a Convention held by adjournments from the 20th day of September, to the 24th of the same inclusive, 1830, in accordance with a public notice issued on behalf of the Coloured Citizens of Philadelphia, and addressed to their brethren throughout the U. States, inviting them to assemble by delegation, in Convention, to be held in the city of Philadelphia, on the 20th day of September, 1830, and signed, on behalf, by the Rev. Bishop Allen, Cyrus Black, Junius C. Morel, Benjamin Paschall, jr. and James Cornish—

The delegation accordingly met in Bethel church, on the 20th September, at 10 o'clock, A. M. and after a chaste and appropriate prayer by the venerable Bishop Allen, the Convention waa organized by electing

Rt. Rev. RICHARD ALLEN, President.

Dr. BELFAST BURTON, of Philadelphia, AUSTIN STEWARD, OF Rochester, N.Y. Vice Presidents.

JUNIUS C. MOREL, of Philadelphia, Secretary, and

ROBERT COWLEY, of Maryland, Assistant Secretary.

On motion it was

Resolved, That this Convention do recommend the formation of a Parent Society ; and that immediately after its organization, to appoint a general corresponding Agent, to reside at or near the intended purchase in Upper Canada.

On motion it was

Resolved, That this Convention enjoins and requires of each of its members to use their utmost influence in the formation of of societies, auxiliary to the Parent Society about being established in the city of Philadelphia; and also to instruct the auxiliary societies when formed, to send delegates to the next General Convention.

On motion it was

Resolved, That the next General Convention shall be composed of delegates appointed by the Parent Society and its auxiliaries: provided always, that the number of delegates from each

iv

society, shall not exceed five, and all other places, where there are no auxiliaries, are hereby invited to send one delegate.

On motion it was

Resolved, That this Convention address the Free People of Colour throughout the United States, and publish in one of the daily papers of this city.

On motion it was

Resolved, That the Convention do adjourn at the invitation of one of the managers of the Lombard-street Free School for coloured children. The Convention were highly gratified at the order, regularity and improvement discoverable in the various departments, among a collection of children, male and female, rising four hundred. Their specimens in writing, needlework, &c. &c. made a deep impression on the Convention, with a desire that the People of Colour may availingly appreciate every extended opportunity for their improvement in the various situations where they may reside.

On motion, the House adjourned sine die.

Rt. Rev. RICHARD ALLEN, President

JUNIUS C. MOREL, Secretary.


The following Delegates composed the Convention, viz.

Pennsylvania—Rev. Richard Allen, Dr. Belfast Burton, Cyrus Black, Junius C. Morel, Benjamin Paschall, jr. James Cornish, Wm. S. Whipper, Peter Gardiner, John Allen, James Newman, Charles H. Leveck, Frederick A. Hinton.

New-York—Austin Steward, Jos. Adams, George L. Brown.

Connecticut—Scipio C. Augustus.

Rhode-Island—George C. Willis, Alfred Niger.

Maryland—James Deavour, Hezekiah Grice, Aaron Willoon, Robert Cowley.

Delaware—Abraham D. Shad.

Virginia—Arthur M. Waring, Wm. Duncan, James West, jr.

HONORARY MEMBERS.

Robert Brown, William Rogers, John Bowers, Richard Howell, Daniel Peterson, Charles Shorts, of Pennsylvania; Leven Williams, of New-York; James P. Walker, of Maryland; John Robinson, of Ohio; Rev. Samuel Todd, of Maryland; John Arnold, of New-Jersey; Sampson Peters, of New-Jersey; Rev. Anthony Campbell, of Delaware; Don Carolos Hall, of Delaware.

CONSTITUTION.

PREAMBLE.

In conformity to a resolution of the Delegates of Free Persons of Colour, in General Convention assembled, in the City of Philadelphia, September 20th, 1830, recommending the formation and establishment of a Parent Society in the City of Philadelphia, for the purpose of purchasing land, and locating a settlement in the Province of Upper Canada; and to which all other Societies formed for that purpose, may become auxiliary—We therefore have adopted the following Constitution.

ARTICLE I.

This Society shall be called "The American Society of Free Persons of Colour, for improving their condition in the United States; for purchasing lands; and for the establishment of a settlement in the Province of Upper Canada:" and shall consist of such Persons of Colour as shall pay not less than twenty five cents on entering, and thereafter quarterly, eighteen and three quarter cents.

ARTICLE II.

The Officers of the Society shall be, a President, and Vice Presidents, four of whom to be chosen out of the city and county of Philadelphia; a Corresponding, Recording, and two Assistant Secretaries, and a Treasurer:a Board of Managers of fifteen members, a Corresponding Committee of five, a Financial Committee of three, a Soliciting Committee of thirteen, and a Publishing Committee of three; all of whom shall be elected by Ballot, at the annual meeting in October.

The Society shall meet quarterly in the city of Philadelphia on the first Monday in October, January, April, and July.

The Board of Managers shall meet to transact business on the last Monday of every month; they shall have power to fill all vacancies occurring during the year, in their body, or any of the committees Nine of their number shall constitute a quorum.

6

ARTICLE III.

The President shall preside at all meetings of the Society, and sign all orders on the Treasurer.

The Vice Presidents shall preside at all meetings of the Society, in the absence of the President.

The President, Vice Presidents, Secretaries, and Treasurer, shall be ex officio members of the Board of Managers.

ARTICLE IV.

The duty of the Coresponding Secretary shall be to attend the meetings of the Corresponding Committee, keep the minutes of their proceedings; he shall be subject to their order, and shall report and present all letters or communications directed to him, to the chairman of the committee, that they may be convened together. He shall also keep a true copy of all his letters or communications.

The Committee of Correspondence shall open an exchange of views with the different Auxiliary Societies that may be formed; receive intelligence concerning the operations of the different societies throughout the United States, and from other persons aiming to improve the situation and condition of the people of colour; and also receive all essays on the subject, with such other information as may conduce to the accomplishment of the great object of the Society.

All communications shall be directed to the Corresponding Secretary.

ARTICLE V.

The Recording Secretary shall attend the meetings of the Society and keep their minutes.

He shall be provided with a book, wherein shall be recorded the proceedings of the Society, of the Board of Managers, and of the Committees, or any persons entrusted with the care or concerns of the Society.

Therefore it shall be the duty of the chairmen of the several committees to aid the Recording Secretary in the discharge of his official duty.

The Assistant Secretaries shall attend the meetings and keep the minutes of the Board of Managers, and assist the Recording Secretary when required.

7

ARTICLE VI.

The Treasurer on entering upon the duties of his office, shall give such security for the faithful performance of his trust as the Board of Managers shall require.

The Treasurer shall not retain in his possession more than $100. All monies above that sum shall be deposited in the United States Bank, that all persons interested in the prosperity of the Institution, may be satisfied as to the safety of their funds; and no sum so deposited shall be withdrawn without an order signed by the President, Vice President, and Secretary of the Parent Society, and four of the Board of Managers thereof.

He shall keep fair accounts of his transactions, hold all papers belonging to the Society, and pay, (if in funds,) all such orders drawn by the Board of Managers, signed by the President, and attested by the Recording Secretary.

He shall annually report to the Board of Managers the state of the treasury, or as often as they may direct; and at the expiration of his term, if not re-elected, shall hand over all the books, papers and funds of the Society to his successor, within thirty days.

ARTICLE VII.

The Financial Committee shall have under their care the pecuniary concerns of the Society, and every thing in relation thereto: they shall also audit the accounts of the Treasurer.

They shall report to the Board of Managers, from time to time, bills or provisions for the increase of the funds, or appropriations of the same, as they may deem in their judgment expedient, that the same may be considered or approved.

ARTICLE VIII.

The Soliciting Committee shall be provided with books for the purpose of receiving subscriptions or donations, wherein shall be registered the names, and amount so received.

ARTICLE IX.

The several Committees shall record, for the future use of the Society, all important observations that may relate to the subject of their charge.

The Board of Managers shall report to the Society quarterly; and at the annual meeting, their report shall be printed in pamphlet form.

8

ARTICLE X.

All Societies, auxiliary to this, shall, when formed, duly notify the Board of Managers of the Parent Society, through its Corresponding Secretary, taking care to forward a copy of their organization and proceedings, to be entered upon the records of the Society.

And with the view of more effectually strengthening a general union among the Free People of Colour, it shall be the duty of each auxiliary Society respectively, to elect from among their own members, one individual as Vice President of the Parent Society.


At a meeting of the Parent Society, held on Monday the 90th of November, 1830, the following persons were elected Officers for the ensuing year, viz.

President—Rev. Richard Allen.

Vice Presidents—Messrs. John Bowers, Rob't Brown, Daniel D. Brownhill, Peter Gardiner.

Corresponding Secretary—William Whipper.

Recording Secretary—Charles H. Leveck.

Assistant Secretaries—John P. Thompson, Samuel D. Potts.

Treasurer—James Johnson.

Board of Managers—Dr. Belfast Burton, Messrs. John P. Burr, Scipio Sewell, John Allen, (Porter,) Richard Howell, Joseph Cassey, Shedrich Basset, James Gibson, Jeremiah Bowser, Richard B. Johnson, James Newman, Henry Beckett, Peter McNeal, James Bird, Abraham Williams.

Corresponding Committee—.Dr. Belfast Burton, Messrs. Dan iel B. Brownhill, John B. Sammons, Frederick A. Hinton, Rev. Richard Allen,

Financial Committee—Messrs. Charles W. Gardner, John B. Sammons, Thomas Butler.

Soliciting Committee—Rev. Richard Allen, Messrs.Samuel Nickels, William James, Joseph Cassey, Thomas Channock, Thomas Butler, William C. West, Robert Johnson, Joshua Brown, Edward Johnson, Jeremiah Bowser, Prince G. Laws, Samuel Combegy.

Publishing Committee—Dr. Belfast Burton, Messrs. William Whipper, John Dutton.

9

CONVENTION OF PEOPLE OF COLOUR

AS much anxiety has prevailed on account of the enactment of laws in several States of the Union, especially that of Ohio, abridging the liberties and privileges of the Free People or Colour, and subjecting them to a series of privations and sufferings, by denying them a right of residence, unless they comply with certain requisitions not exacted of the Whites, a course altogether incompatible with the principles of civil and religious liberty.

In consideration of which, a delegation* was appointed from the states of Connecticut, New York, Pennsylvania, Delaware, and Maryland, to meet in Convention in Philadelphia, to consider the propriety of forming a settlement in the province of Upper Canada, in order to afford a place of refuge to those who may be obliged to leave their homes, as well as to others inclined to emigrate with the view of improving their condition

The said Convention accordingly met in Bethel Church, city of Philadelphia, on the 20th of September, 1830; and having fully considered the peculiar situation of many of their brethren, and the advantages to be derived from the proposed settlement, adopted the following

ADDRESS

To the Free People of Colour of these United States.

Brethren,

Impressed with a firm and settled conviction, and more especially being taught by that inestimable and invaluable instrument, namely, the Declaration of Independence, that all men are born free and equal, and consequently are endowed with unalienable rights, among which are the enjoyments of life, liberty, and the pursuits of happiness.

Viewing these as incontrovertable facts, we have been led to the following conclusions; that our forlorn and deplorable situation earnestly and loudly demand of us to devise and pursue all legal means for the speedy elevation of ourselves and brethren to the scale and standing of men.

In consequence of not having had timely notice, delegates from other sections of the country did not attend; though it is hoped that at the Convention on the first Monday of June next, there will be a more general representation.

10

And in pursuit of this great object, various ways and means have been resorted to; among others, the African Colonization Society is the most prominent. Not doubting the sincerity of many friends who are engaged in that cause; yet we beg leave to say, that it does not meet with our approbation. However great the debt which these United States may owe to injured Africa, and however unjustly her sons have been made to bleed, and her daughters to drink of the cup of affliction, still we who have been born and nurtured on this soil, we, whose habits, manners, and customs are the same in common with other Americans, can never consent to take our lives in our hands, and be the bearers of the redress offered by that Society to that much affiicted country.

Tell it not to barbarians, lest they refuse to be civilised, and eject our christian missionaries from among them, that in the nineteenth century of the christian era, laws have been enacted in some of the states of this great republic, to compel an unprotected and harmless portion of our brethren, to leave their homes and seek an asylum in foreign climes: and in taking a view of the unhappy situation of many of these, whom the oppressive laws alluded to, continually crowd into the Atlantic cities, dependent for their support upon their daily labour, and who often suffer for want of employment, we have had to lament that no means have yet been devised for their relief.

These considerations have led us to the conclusion, that the formation of a settlement in the British province of Upper Canada, would be a great advantage to the people of colour. In accordance we pledge ourselves to aid each other by all honourable means, to plant and support one in that country, and therefore we earnestly and mostly feelingly appeal to our coloured brethren, and to all philanthropists here and elsewhere, to assist in this benevolent and important work.

To encourage our brethren earnestly to co-operate with us, we olfer the following, viz. 1st. Under that government no invidious distinction of colour is recognised, but there we shall be entitled to all the rights, privileges, and immunities of other citizens. 2d. That the language, climate, soil, and productions are similar to those in this country, 3d. That land of the best quality can be purchased at the moderate price of one dollar and fifty cents per acre, by the one hundred acres. 4th. The market for different kinds of produce raised in that colony, is such as to render a

11

suitable reward to the industrious farmer, equal in our opinion to that of the United States. And lastly, as the erection of buildings must necessarily claim the attention of the emigrants, we would invite the mechanics from our large cities to embark in the enterprise; the advancement of architecture depending much on their exertions, as they must consequently take with them the arts and improvements of our well regulated communities.

It will be much to the advantage of those who have large families, and desire to see them happy and respected, to locate themselves in a land where the laws and prejudices of society will have no elfect in retarding their advancement to the summit of civil and religious improvement. There the diligent student will have ample opportunity to reap the reward due to industry and perseverence; whilst those of moderate attainments, if properly nurtured, may be enabled to take their stand as men in the several offices and situations necessary to promote union, peace, order and tranquility. It is to these we must look for the strength and spirit of our future prosperity.

Before we close, we would just remark, that it has been a subject of deep regret to this convention, that we as a people have not availingly appreciated every opportunity placed within our power by the benevolent efforts of the friends of humanity, in elevating our condition to the rank of freemen. That our mental and physical qualities have not been more actively engaged in pursuits more lasting, is attributable in a great measure to a want of unity among ourselves; whilst our only stimulus to action has been to become domestics, which at best is but a precarious and degraded situation.

It is to obviate these evils, that we have recommended our views to our fellow-citizens in the foregoing instrument, with a desire of raising the moral and political standing of ourselves; and we cannot devise any plan more likely to accomplish this end, than by encouraging agriculture and mechanical arts: for by the first, we shall be enabled to act with a degree of independence, which as yet has fallen to the lot of but few among us; and the faithful pursuit of the latter, in connection with the sciences, which expand and ennoble the mind, will eventually give us the standing and condition we desire.

To effect these great objects, we would earnestly request our brethren throughout the United States, to co-operate with us, by forming societies auxiliary to the Parent Institution, about being established in the city of Philadelphia, under the patronage of the GENERAL CONVENTION. And we further recommend to our friends and brethren, who reside in places where, at present, this may be impracticable, so far to aid us, by contributing to the funds of the Parent Institution; and, if disposed, to appoint one delegate to represent them in the next Convention, to be held in Philadelphia the first Monday in June next, it being fully understood, that organized societies be at liberty to send any number of delegates not exceeding five.

Signed by order of the Convention,

Rev. RICHARD ALLEN, President, Senior Bishop or the African Methodist Episcopal Churches.

JUNlUS C. MOREL, Secretary.
"""

#Add Obfuscation - Add tag
#obfuscate_function(heading,"h1")
obfuscate_function(body,"p")

#End the HTML File
to_html.append("</html>")

#Save the HTML File
file = open('obfuscation.html','w')
for i in to_html:
    file.write(str(i))
file.close()


