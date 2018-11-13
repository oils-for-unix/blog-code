#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <sys/mman.h>  // mmap()
#include <unistd.h>  // write()
#include <string.h>  // strlen()

const int MAX_LINE = 1024;

void CountLines(char* buf, size_t num_bytes) {
    int num_lines = 0;
    char* cur = buf;
    char* end = buf + num_bytes;

    while (cur < end){
      if (*cur == '\n') {
        num_lines++;
      }
      cur++;
    }
    fprintf(stderr, "num_lines = %d\n", num_lines);
}

/*!re2c
  re2c:define:YYCTYPE = "char";
  re2c:define:YYCURSOR = p;
  re2c:yyfill:enable = 0;  // generated code doesn't ask for more input
*/

void GrepFixedStrings(char* buf, size_t num_bytes) {
  char* p = buf;
  char* end = buf + num_bytes;
  char* end1 = end-1;

  char* YYMARKER;

  int num_lines = 0;
  int num_keywords = 0;
  int nothing = 0;

  bool print_line = false;

  // NOTE: I tried the "goto loop/goto done" instead of "continue/break", but
  // it didn't speed it up.
  for (;;) {
    /*!re2c

      "earthly" | "watermark" | "monetarism" | "rumbles" | "Karl" | "kits" | "foyers" | "troubadours" | "anemic" | "Michigan" | "timelessness" | "bribe" | "reinterprets" | "faculties" | "tornados" | "gallstone" | "gigglers" | "amnesiacs" | "chit" | "rums" | "prioritizes" | "bulling" | "objections" | "jumping" | "bloodstains" | "defensing" | "vacua" | "surmised" | "tansy" | "Trey" | "aneurisms" | "countersinking" | "turmoils" | "perk" | "relativistic" | "hyacinth" | "accomplishing" | "blitzed" | "funereal" | "dilution" | "corrected" | "elopements" | "whackiest" | "refutations" | "Namath" | "headstones" | "compresses" | "peck" | "perambulators" | "unnerves" | "consorts" | "penitently" | "mercurial" | "Brailles" | "resulting" | "Bridger" | "baggage" | "cowed" | "inroads" | "euphemisms" | "Zion" | "zero" | "snarl" | "multiplied" | "splashdown" | "escrow" | "patriarchs" | "homerooms" | "prettier" | "diarrhoea" | "helpers" | "flaunted" | "Congress" | "beau" | "dowelled" | "canisters" | "retells" | "spectacular" | "reserves" | "dulness" | "schmalzy" | "modernizes" | "unfounded" | "surfer" | "sweetie" | "piping" | "scrapers" | "conducing" | "enamors" | "braked" | "roadblocked" | "instructed" | "hollyhocks" | "prizefighting" | "eyeing" | "heritages" | "tenderized" | "pitch" | "swills" | "scuffled" | "pits" | "crudity" | "actuary" | "barrios" | "agonies" | "discrepancies" | "inscription" | "clamoring" | "carboy" | "sliver" | "persevering" | "slapping" | "hostess" | "nativities" | "hellholes" | "amputate" | "grackles" | "impala" | "explicit" | "beheading" | "curiously" | "refurnishes" | "disloyal" | "panel" | "workhorse" | "evicting" | "illumination" | "Weston" | "sharked" | "oncology" | "profusely" | "nite" | "loggerheads" | "parochial" | "rewording" | "shooting" | "obstetrical" | "plains" | "mangroves" | "sociopaths" | "puerility" | "woodcuts" | "nasalizes" | "groves" | "sealants" | "Gordian" | "McNamara" | "absconding" | "reunifying" | "Alexander" | "astronomer" | "methadon" | "Phekda" | "relive" | "Paley" | "squinting" | "Marina" | "Schwarzkopf" | "squashy" | "accented" | "swaths" | "vividly" | "unflinchingly" | "traumas" | "sourest" | "ransacking" | "Johnston" | "furthering" | "bunks" | "weeknights" | "scrimped" | "oilfield" | "imperilled" | "Moira" | "statistical" | "transpose" | "Casandra" | "discriminated" | "bevy" | "insecurity" | "windowpanes" | "slaughterhouses" | "hairbrushes" | "feller" | "heightening" | "disinter" | "glitters" | "dispels" | "thumps" | "voluptuous" | "histogram" | "cased" | "anchor" | "croquettes" | "emphasized" | "commanders" | "watchmaker" | "protrude" | "turfing" | "perigees" | "Augean" | "bombers" | "baroque" | "meetings" | "bogeyed" | "lowered" | "Moriarty" | "subhead" | "wailing" | "solariums" | "clicks" | "recidivist" | "chemists" | "interdicts" | "consumables" | "monographs" | "Chayefsky" | "perfections" | "Squibb" | "lettuce" | "oracle" | "unholy" | "toughens" | "malefactor" | "burbled" | "regurgitated" | "menial" | "learned" | "beetles" | "typecasting" | "antigens" | "callipers" | "apparel" | "denounced" | "dullness" | "stoles" | "Issachar" | "Eleazar" | "catchiest" | "farmed" | "meat" | "availed" | "twelves" | "armrests" | "forthwith" | "Episcopalians" | "juggernaut" | "edema" | "wisecracking" | "litigiousness" | "Hispaniola" | "pegging" | "tares" | "dreamier" | "appraisers" | "Myra" | "massed" | "niftier" | "impetigo" | "bragger" | "devilled" | "overgrowth" | "immovable" | "Geiger" | "opaqueness" | "Kublai" | "prematurely" | "foppish" | "limerick" | "shag" | "quintuplets" | "farmhand" | "Bathsheba" | "Judy" | "detriment" | "heralding" | "misdoing" | "parishioner" | "livelihood" | "vestigial" | "sake" | "tailspin" | "overwork" | "shafting" | "marquess" | "cerebella" | "Talmudic" | "howdah" | "insensitively" | "undershorts" | "urinalyses" | "bowstring" | "sated" | "hesitatingly" | "plunks" | "forfeits" | "Wilkes" | "legions" | "fumigator" | "fetishism" | "lasers" | "bucketful" | "blinking" | "Stendhal" | "actuators" | "overtimes" | "spotter" | "Priscilla" | "souring" | "abrading" | "proportioning" | "postpaid" | "Iraqis" | "Italian" | "premium" | "metabolize" | "Boleyn" | "sunset" | "pastoral" | "tourneys" | "snappiest" | "outdoors" | "Eton" | "ottoman" | "amputee" | "nonseasonal" | "Wittgenstein" | "mislays" | "humaneness" | "roes" | "wingers" | "tiptop" | "psychoanalyzes" | "complainant" | "Powhatan" | "dawns" | "doggone" | "rearm" | "pastern" | "operands" | "ambulatory" | "reenforces" | "volunteering" | "biggest" | "forgotten" | "Beerbohm" | "involvements" | "salesgirls" | "curling" | "chief" | "Slovenians" | "guarantor" | "underachiever" | "logging" | "rightest" | "Loraine" | "flamboyance" | "truant" | "Earhart" | "gangrening" | "magazine" | "clinches" | "acquaintance" | "dubiously" | "excavation" | "fraternize" | "Popsicle" | "gorgeous" | "symposium" | "humidors" | "appointed" | "kooks" | "shimmery" | "mileposts" | "weirdest" | "airsickness" | "scrapbooks" | "applicable" | "watchband" | "Walt" | "palsies" | "rigor" | "soviets" | "swanky" | "variably" | "finishes" | "tummy" | "frigid" | "administer" | "shaken" | "fondants" | "hireling" | "saber" | "empire" | "mongeese" | "Trent" | "deducing" | "broker" | "ballsier" | "Jerusalem" | "Farrell" | "olfactory" | "stickleback" | "videodisc" | "understandings" | "fawning" | "prosperously" | "winner" | "Little" | "pedestrian" | "hiccup" | "egret" | "stumbling" | "anchorites" | "dudes" | "quivering" | "throb" | "merchantmen" | "adultery" | "ungrateful" | "castration" | "squealing" | "absurdest" | "adequately" | "genuflected" | "server" | "equitable" | "faithfully" | "manifestoes" | "caroming" | "retypes" | "nosing" | "woodworking" | "Darnell" | "forsooth" | "assiduousness" | "nitpicking" | "heathenish" | "enjoining" | "vaguely" | "Elias" | "gimmicky" | "mandrill" | "huntsmen" | "furry" | "bouillabaisses" | "tailgated" | "lesion" | "spellbinders" | "offensiveness" | "sophistry" | "unforgettably" | "trims" | "privately" | "Gounod" | "archers" | "Scottish" | "factitious" | "stuttered" | "chubby" | "capacitors" | "remonstrate" | "magnifiers" | "tamps" | "statuettes" | "artier" | "greening" | "beaches" | "bulimia" | "jibbing" | "seashores" | "street" | "Jews" | "begrudging" | "extrudes" | "skirt" | "abide" | "vengeful" | "Herbert" | "daubed" | "degenerated" | "doggoning" | "barring" | "flimsier" | "Moore" | "optimizes" | "tracker" | "geologist" | "Hellman" | "coves" | "punt" | "bonbon" | "imprecations" | "tacks" | "skidding" | "Lolita" | "Ganges" | "nineteenth" | "potshots" | "Frye" | "firefight" | "evaporates" | "bast" | "Oscars" | "resisted" | "Hale" | "amaryllis" | "hoarder" | "festering" | "cyclical" | "kilometer" | "neediest" | "briefings" | "diners" | "Melanesian" | "spluttered" | "jacking" | "Winfred" | "earfuls" | "objectionable" | "matrices" | "metallurgist" | "terrorist" | "strangling" | "substrate" | "blurt" | "disastrously" | "tonality" | "flourishes" | "modulations" | "gleamings" | "hydrangeas" | "Occam" | "Schneider" | "quarterbacking" | "vans" | "continued" | "manor" | "encore" | "Leola" | "negotiable" | "typesetting" | "formidably" | "credulity" | "legitimize" | "solution" | "sidings" | "sportsmanlike" | "Januaries" | "vibrated" | "contacts" | "bookmaker" | "blued" | "mistaking" | "insane" | "outranking" | "wrongfully" | "sackcloth" | "savoring" | "excruciating" | "sexy" | "Daedalus" | "dogie" | "perjurers" | "droller" | "lamentably" | "incongruously" | "blastoff" | "scruff" | "beckoned" | "Dodoma" | "ecologically" | "roil" | "infertile" | "sorcery" | "wade" | "Kong" | "demotions" | "informant" | "hurl" | "backpedalling" | "Minos" | "curtseying" | "inexhaustible" | "greater" | "bigotry" | "Cartwright" | "workaholics" | "dictate" | "capsuling" | "inadvertently" | "howls" | "anesthetics" | "fabulously" | "Sumner" | "Tombaugh" | "Honduras" | "asphalt" | "spilled" | "unpin" | "coordinators" | "cherries" | "rationalists" | "overcooks" | "landmass" | "Cormack" | "sprinter" | "avowals" | "emptiness" | "chattels" | "deigns" | "gaudily" | "market" | "rationalist" | "untried" | "grinning" | "thunderclap" | "malleability" | "isles" | "dilatory" | "indispensables" | "headmistress" | "preciousness" | "besot" | "skewed" | "stepsisters" | "disusing" | "sawhorses" | "stigmatized" | "wheezes" | "harlot" | "bishoprics" | "salted" | "elephantine" | "waggish" | "pebbling" | "Kawabata" | "caesurae" | "defined" | "Valkyrie" | "Todd" | "Aron" | "computer" | "manifest" | "liberal" | "incite" | "chary" | "peptic" | "connotations" | "Cleo" | "ballads" | "satirist" | "ensues" | "grossness" | "numbskull" | "endless" | "booklet" | "humbugged" | "Araceli" | "emphysema" | "stomach" | "reiteration" | "Molina" | "loads" | "braise" | "cleric" | "replicating" | "entered" | "recursive" | "eminences" | "clubbing" | "proctors" | "Nigel" | "stashed" | "indistinctly" | "ugliness" | "horrible" | "rigidity" | "Adenauer" | "collusion" | "lethargically" | "takeover" | "represents" | "Dracula" | "attractively" | "adulterant" | "hatching" | "monied" | "induction" | "zincing" | "seaward" | "epitomize" | "additional" | "timings" | "decentralize" | "Technicolor" | "befall" | "Elbe" | "miaowing" | "deteriorate" | "taker" | "creditors" | "wombats" | "mumbles" | "blackens" | "depositor" | "indicted" | "budgerigar" | "altos" | "Siamese" | "tablespoon" | "rowdy" | "weighty" | "denouncements" | "innate" | "filch" | "fulminated" | "shanghaied" | "convalescing" | "horizontally" | "revengeful" | "deviations" | "shutting" | "Moroccans" | "surliest" | "Cadillac" | "peppy" | "coxcombs" | "burn" | "shoe" | "garnishees" | "abates" | "outperformed" | "ingenuously" | "lumpier" | "cupsful" | "novelty" | "achievable" | "rheostats" | "unrecognizable" | "bureaucratic" | "columbine" | "discords" | "blandly" | "vassalage" | "burns" | "aggrandizes" | "confuse" | "jukebox" | "refunds" | "needy" | "zoological" | "Acapulco" | "paneled" | "bonds" | "prepackages" | "explodes" | "preoccupied" | "Commons" | "discourteous" | "Stacy" | "brusquely" | "fortified" | "powerboat" | "bacterias" | "breaststrokes" | "doublets" | "elicited" | "courser" | "samples" | "tonier" | "lobe" | "mourners" | "Brest" | "chucks" | "Cagney" | "Jackie" | "bewildered" | "congregating" | "sloppiest" | "straddles" | "dirties" | "perambulate" | "laze" | "instructing" | "Germany" | "nannies" | "serialize" | "favorite" | "heart" | "Sheraton" | "fiendish" | "zigzagging" | "sifters" | "muffins" | "advertises" | "shaking" | "blacked" | "tribalism" | "intellects" | "strode" | "foreshadow" | "verdigrised" | "cast" | "overwhelming" | "lowercase" | "ruined" | "berths" | "saga" | "laboriously" | "Condorcet" | "innovative" | "cascading" | "birdie" | "miscuing" | "germs" | "tarred" | "ferrules" | "Burns" | "vindicate" | "brig" | "nullity" | "petting" | "Hakka" | "Macedon" | "arrangement" | "ballrooms" | "Polaroids" | "pilasters" | "mark" | "dusts" | "biodiversity" | "hard" | "governors" | "Israels" | "sapphire" | "polluters" | "immaturely" | "convalesced" | "silted" | "peak" | "globule" | "multiple" | "muscle" | "leash" | "Zulus" | "superstructures" | "cantatas" | "longboats" | "souping" | "import" | "quieted" | "handicrafts" | "unworthier" | "practical" | "secessionists" | "sorceress" | "chaperons" | "wingspread" | "holocaust" | "ovals" | "commenting" | "spraining" | "sandmen" | "methadone" | "iguana" | "Aeneid" | "nurturing" | "dioramas" | "reshuffling" | "Rudolph" | "Sontag" | "placentas" | "airworthy" | "swamps" | "whoops" | "parrot" | "backslappers" | "dancers" | "found" | "shadow" | "infantries" | "carver" | "workable" | "prepossesses" | "Gael" | "shrillest" | "neuroses" | "evils" | "odious" | "George" | "quads" | "altho" | "clapboarding" | "enhancer" | "girlish" | "Camacho" | "Sexton" | "vomits" | "apologist" | "panelled" | "magnanimous" | "Carol" | "annoyed" | "demagnetization" | "unsubscribing" | "dulcimers" | "expectations" | "fussily" | "Louisville" | "reliving" | "opposite" | "pedicure" | "conciliator" | "aggravating" | "rampart" | "windbreak" | "Revlon" | "linearly" | "relating" | "underemployed" | "rhinoceros" | "procreation" | "stripes" | "Alyce" | "hypnoses" | "ovum" | "gullies" | "that" | "Rankine" | "puttying" | "crouching" | "condescension" | "wigwagging" | "varlets" | "fluids" | "registry" | "landscapers" | "epilogue" | "divas" | "preened" | "tinge" | "schoolmasters" | "sachems" | "Candace" | "insinuating" | "mattering" | "bolster" | "reunites" | "traipses" | "modernistic" | "demagog" | "Marley" | "Argentinians" | "abolish" | "brittlest" | "mute" | "cheeseburgers" | "digestible" | "invade" | "initiations" | "axioms" | "wirelesses" | "Angolan" | "startling" | "spraying" | "admiralty" | "gracious" | "jeopardy" | "Marianas" | "Missy" | "Siddhartha" | "boycotts" | "restructures" | "expound" | "peephole" | "powders" | "uncleanlier" | "suffrage" | "Wobegon" | "construed" | "assistants" | "unexceptionable" | "crullers" | "Solomon" | "submerge" | "rectifiers" | "anarchistic" | "twits" | "Anglo" | "flattops" | "rigging" | "billfolds" | "copyrights" | "tangoing" | "refuted" | "agonizingly" | "maria" | "discs" | "begrudged"  // __TO_REPLACE__ 
      {
        num_keywords++;
        continue;
      }
      "\n"  {
         print_line = false;
         num_lines++;
         if (p >= end1) break;
         continue;
      }
      * {
        // NOTE: states are reordered so we need continue everywhere.
        continue;
      }
    */
  }
  fprintf(stderr, "num_lines = %d\n", num_lines);
  fprintf(stderr, "num_keywords = %d\n", num_keywords);
  fprintf(stderr, "nothing = %d\n", nothing);
}


int main(int argc, char **argv) {
  if (argc == 0) {
    printf("Expected filename\n");
    return 1;
  }
  char* action = argv[1];

  FILE *f = fopen(argv[2], "rb");
  if (!f) {
    printf("Error opening %s\n", argv[1]);
    return 1;
  }

  fseek(f, 0, SEEK_END);
  size_t num_bytes = ftell(f);
  fseek(f, 0, SEEK_SET);  //same as rewind(f);

  int fd = fileno(f);

  if (strcmp(action, "read:re2c-match") == 0) {  // read
    char* buf = (char*)malloc(num_bytes);
    size_t num_read = read(fd, buf, num_bytes);

    GrepFixedStrings(buf, num_bytes);

    fprintf(stderr, "num_bytes = %zu\n", num_bytes);
    //free(buf);

    return 0;
  } 

  if (strcmp(action, "read:count-lines") == 0) {  // read
    char* buf = (char*)malloc(num_bytes);
    size_t num_read = read(fd, buf, num_bytes);

    CountLines(buf, num_bytes);

    fprintf(stderr, "num_bytes = %zu\n", num_bytes);
    //free(buf);

    return 0;
  } 

  if (strcmp(action, "fgets") == 0) {
    char line[MAX_LINE]; 
    while (fgets(line, MAX_LINE, f)) {
      //printf("string is: %s\n", buf); 
      //puts(line);
      fputs(line, stdout);
      //write(1, line, strlen(line));
    }

    return 0;
  }
  
  if (strcmp(action, "mmap") == 0) {  // mmap

    //int fd = open(argv[1], O_RDONLY, 0);
    //assert(fd != -1);
    //Execute mmap
    char* buf = (char*)mmap(NULL, num_bytes, PROT_READ, MAP_PRIVATE | MAP_POPULATE, fd, 0);
    assert(buf != MAP_FAILED);

    // 963 ms on all-10.txt.  Hm OK.
    //CountLines(buf, num_bytes);

    // 969 ms with a couple keywords.  Not slower.
    // But if I add like 10 keywords, then it's 2.3 seconds!  Slower than
    // fgrep!

    // fgrep is over a second too though.
    GrepFixedStrings(buf, num_bytes);

    //Write the mmapped data to stdout (= FD #1)
    //size_t out = write(1, buf, num_bytes);

    //Cleanup
    int rc = munmap(buf, num_bytes);
    if (rc != 0) {
      perror("Error munmap:");
    }
    //close(fd);

    return 0;
  }

  fclose(f);

  fprintf(stderr, "Invalid action");
  return 1;
}
