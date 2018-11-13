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

      "buttoned" | "incidentally" | "noblest" | "abrupt" | "motocross" | "actionable" | "shudders" | "flogs" | "basins" | "somewhere" | "shantytown" | "bilateral" | "montages" | "nerve" | "megaliths" | "mermaids" | "Yenisei" | "lettered" | "loco" | "miming" | "Walmart" | "preclusion" | "remembers" | "clang" | "dusk" | "piazze" | "prizefights" | "album" | "leggin" | "craw" | "patellas" | "needlework" | "safeness" | "cabs" | "incessant" | "mollycoddled" | "digestive" | "argue" | "occlude" | "palest" | "persist" | "schlepping" | "mispronounce" | "monsieur" | "bathing" | "firmware" | "booziest" | "kosher" | "windsurfing" | "grinned" | "slattern" | "Carlsbad" | "jest" | "Biblical" | "Downs" | "Pele" | "undeceiving" | "drones" | "aridity" | "sloped" | "housebreaking" | "stressful" | "incrusts" | "Jesuits" | "bedecked" | "tanneries" | "Passover" | "knob" | "Donovan" | "horsetails" | "Regor" | "genially" | "effusions" | "brackish" | "warn" | "haired" | "mixtures" | "embarkation" | "expostulated" | "Lizzy" | "forsaken" | "snowplowing" | "consonance" | "reviews" | "satiety" | "deified" | "stripteases" | "fictional" | "jets" | "roadblocking" | "reassuring" | "faithlessness" | "styles" | "catty" | "terraces" | "Merthiolate" | "tannery" | "theatre" | "shareholder" | "sulfates" | "scalawag" | "precipitant" | "steely" | "unpredictable" | "closets" | "detoxed" | "Laius" | "conjunctions" | "critiqued" | "corduroys" | "girdle" | "hindquarter" | "raided" | "puppets" | "fuselages" | "synthesizers" | "blisters" | "pirating" | "misprints" | "clams" | "rarefy" | "stockier" | "playground" | "recompiled" | "reject" | "imperishable" | "sunless" | "vetted" | "avid" | "Burger" | "rueful" | "Sindhi" | "huskier" | "Wall" | "Saskatchewan" | "continuations" | "conceptually" | "slumping" | "rusted" | "semiweeklies" | "coercive" | "pica" | "Otis" | "tigress" | "Lambert" | "Lorraine" | "Madison" | "previewer" | "oozed" | "slues" | "poetic" | "computing" | "antique" | "wayfaring" | "loyaler" | "delineate" | "crankiness" | "barrage" | "photocopier" | "patty" | "Padilla" | "funniest" | "attraction" | "reducing" | "halved" | "typhus" | "curst" | "tiptops" | "microorganisms" | "developer" | "fiercer" | "Elam" | "tweeter" | "retain" | "tranquilizing" | "inorganic" | "farcical" | "indifferently" | "hawked" | "philosophy" | "killers" | "chirping" | "ingratiated" | "doggone" | "Chad" | "Olive" | "Galsworthy" | "extraneously" | "copyrights" | "boastfulness" | "innings" | "inanity" | "spokespersons" | "snorkelled" | "tragedian" | "rumor" | "outshined" | "vanes" | "expressways" | "discombobulates" | "jackasses" | "pessimistic" | "bombing" | "theatrical" | "streaming" | "amazement" | "selvedges" | "Malraux" | "Grus" | "totems" | "convent" | "lecterns" | "winnow" | "rococo" | "Rooney" | "commend" | "Alfred" | "microscopic" | "mistranslated" | "twang" | "Cambridge" | "foreground" | "gestates" | "manipulative" | "whets" | "extorts" | "cowgirls" | "bogeyed" | "constriction" | "size" | "checkout" | "demography" | "wrongdoers" | "conquered" | "straightjackets" | "Herod" | "whether" | "activist" | "petrochemical" | "Kickapoo" | "ours" | "Paleozoic" | "imagine" | "philosophers" | "foils" | "rephrasing" | "decree" | "choosier" | "plutocracy" | "pirouette" | "clashed" | "cousins" | "gofer" | "taxies" | "lutes" | "tiros" | "helical" | "savant" | "today" | "dissolve" | "freebie" | "wrigglier" | "Korea" | "gaze" | "rustproofed" | "divine" | "reordered" | "dullest" | "dustpans" | "comparisons" | "drawings" | "tensor" | "brigs" | "colliding" | "reusable" | "stallions" | "unbend" | "sampling" | "braining" | "lineups" | "barrener" | "melodrama" | "polyphonic" | "broadcasters" | "daybed" | "interview" | "Jarred" | "Tyre" | "headset" | "refocussing" | "Renaissances" | "lobster" | "clunkers" | "unbiassed" | "unbent" | "divergence" | "cobble" | "afflicts" | "Rothschild" | "exercised" | "scrubbier" | "borrowing" | "slandering" | "rapping" | "signature" | "debenture" | "heuristics" | "complemented" | "explicate" | "crutches" | "achievers" | "reassemble" | "aureoles" | "gainsay" | "tightened" | "clerics" | "carnivorous" | "sociology" | "incalculable" | "fellows" | "related" | "jackets" | "Huggins" | "coeval" | "vandals" | "matron" | "suppuration" | "ambushing" | "Mister" | "Corning" | "bondsman" | "eccentricities" | "twinning" | "wheaten" | "suffices" | "obstetrical" | "suitably" | "tendons" | "Copland" | "abetted" | "vaccines" | "printed" | "informs" | "rebound" | "intently" | "fetich" | "recover" | "balsas" | "Unitarians" | "woodpeckers" | "stuffily" | "nonesuch" | "geologically" | "moms" | "Yokohama" | "Waite" | "infotainment" | "cicadas" | "novella" | "cellular" | "solubility" | "doubtfully" | "kilobyte" | "colonizing" | "undergarments" | "golly" | "Baguio" | "wimp" | "spurned" | "prof" | "gluttony" | "reaffirmed" | "electroencephalographs" | "background" | "weatherize" | "japanning" | "chowders" | "hardliners" | "homecoming" | "rhythms" | "eggplant" | "blissfully" | "kingdoms" | "itch" | "Guallatiri" | "repeats" | "overlie" | "womanizes" | "systolic" | "lavender" | "Wise" | "condoles" | "pledge" | "marched" | "delays" | "fluid" | "Merriam" | "Kalahari" | "livens" | "precariously" | "suppleness" | "crackdown" | "jingles" | "indecency" | "nonpartisans" | "assume" | "pill" | "adman" | "scum" | "salmonella" | "scrunching" | "gloriously" | "Bumppo" | "observer" | "sophism" | "boggy" | "evacuates" | "featherweight" | "catnap" | "bewitches" | "hulk" | "landscaped" | "Markab" | "peed" | "stumpier" | "Lippi" | "servo" | "wreathing" | "adorns" | "Sardinia" | "pines" | "overachieves" | "Schiaparelli" | "Baal" | "tablespoonfuls" | "Parker" | "snugger" | "uptakes" | "uptight" | "exhibition" | "dweeb" | "certified" | "Bandung" | "highly" | "antiquity" | "piccolo" | "schoolmate" | "wrapt" | "reciprocal" | "implacably" | "fight" | "postmark" | "cliffs" | "resignation" | "recommend" | "teapot" | "rucksacks" | "receptionist" | "tithing" | "misstate" | "taps" | "collate" | "cudgeling" | "confound" | "boor" | "nonmalignant" | "refute" | "barest" | "receipting" | "Paraguay" | "plushest" | "awarded" | "dormouse" | "likest" | "scruffs" | "wisecracks" | "problematically" | "depopulation" | "hippopotamus" | "equable" | "slow" | "assail" | "Sephardi" | "cardboard" | "Trudy" | "tiled" | "storage" | "disrobes" | "frameworks" | "voluminous" | "panther" | "airing" | "scatterbrained" | "meters" | "tremulous" | "unacceptably" | "raft" | "Douala" | "Ujungpandang" | "screech" | "uttermost" | "braggarts" | "struggled" | "gardener" | "Macaulay" | "choosy" | "tiller" | "slay" | "elevates" | "cabby" | "Tussaud" | "commander" | "scrawniest" | "Freeman" | "indenture" | "tinning" | "hospitalized" | "slinkier" | "aerated" | "loners" | "settlement" | "explicitness" | "depot" | "daredevils" | "lifeboats" | "Johnnie" | "contumely" | "distributive" | "Plato" | "nonnegotiable" | "Canada" | "handily" | "hazelnut" | "transducer" | "brushes" | "kinematics" | "shade" | "counteraction" | "abundant" | "Goff" | "determiner" | "incapacitating" | "disband" | "speculation" | "reopening" | "shallots" | "edgeways" | "burnooses" | "networked" | "bookshops" | "underworld" | "excursions" | "Pepys" | "pelvis" | "unstopped" | "pigged" | "whimsical" | "businesswoman" | "vatted" | "restock" | "inferiority" | "brides" | "bankrupts" | "crosier" | "occupies" | "raids" | "breathiest" | "snuggled" | "ovarian" | "redistrict" | "apathy" | "esplanades" | "horn" | "disrobed" | "ventilators" | "persecute" | "haloing" | "attention" | "mukluk" | "coax" | "chairmen" | "empanels" | "detrimental" | "exhaustively" | "fledgeling" | "ruefully" | "corpus" | "yacked" | "pompously" | "acclimates" | "entrances" | "induction" | "flimflam" | "morn" | "manipulators" | "Bret" | "vault" | "catacomb" | "charring" | "Lesotho" | "Bangor" | "maternal" | "hideout" | "perpetrates" | "primacy" | "intents" | "rapier" | "tawniest" | "filaments" | "militantly" | "interpreting" | "timezone" | "dandy" | "effusively" | "bookshelves" | "bighearted" | "rejoicings" | "polka" | "chemists" | "intermarriage" | "Bruno" | "conjugate" | "answerable" | "Phipps" | "Rickenbacker" | "iridescent" | "letdown" | "Airedales" | "parrot" | "uninterpreted" | "murderesses" | "glorify" | "Rivers" | "aquariums" | "metastasized" | "hapless" | "bandits" | "barrettes" | "jabots" | "Islamic" | "telegraph" | "Manhattan" | "warp" | "Russel" | "subsequent" | "tinglier" | "Alcibiades" | "Kasai" | "Blantyre" | "fenders" | "volatility" | "straggle" | "Edwin" | "lodestone" | "prolific" | "wavelets" | "workbench" | "imperceptible" | "resiliency" | "motorcycles" | "Bulganin" | "limp" | "prey" | "Santa" | "truest" | "bespoke" | "fathomable" | "bassos" | "shuffleboard" | "anteed" | "tortures" | "wigwams" | "tougher" | "gibbons" | "seafarer" | "singularly" | "headwind" | "journeyed" | "squished" | "zeroed" | "facility" | "savvier" | "capitalists" | "semicolons" | "considerate" | "morality" | "interminable" | "proportionately" | "condoned" | "scrapbook" | "polonaise" | "sought" | "quirky" | "accommodates" | "Absalom" | "greedily" | "reveler" | "subliming" | "devises" | "magnificence" | "flat" | "reheats" | "sepsis" | "greengrocer" | "personally" | "unlisted" | "campsite" | "stash" | "catacombs" | "humiliated" | "Steiner" | "communes" | "Pacino" | "decent" | "shilled" | "Lottie" | "sharpen" | "sanitation" | "mordant" | "kinetic" | "vestment" | "circulates" | "floodlights" | "abjuration" | "reflections" | "emits" | "smokestack" | "wantonness" | "flatboat" | "nattiest" | "alpacas" | "nonchalant" | "flashier" | "variously" | "Ellie" | "elocutionist" | "digitally" | "hunk" | "liquify" | "trowelling" | "physiologist" | "directer" | "revile" | "skinless" | "gorges" | "bicameral" | "venality" | "tequilas" | "exploded" | "clairvoyants" | "monoxide" | "comet" | "slammed" | "Gamow" | "feasibility" | "haemorrhoids" | "sunlit" | "trucked" | "linen" | "incompetently" | "truckling" | "Pontianak" | "seismic" | "colloid" | "pommelled" | "Austen" | "touching" | "cherub" | "urchin" | "becomes" | "downhills" | "credenza" | "tenure" | "restart" | "sari" | "strangely" | "Taine" | "nonsectarian" | "papers" | "unannounced" | "ousts" | "toted" | "mutilate" | "flagstones" | "bandaging" | "gassed" | "grasses" | "davenports" | "reappears" | "Ferris" | "dolly" | "angular" | "Herschel" | "refrigerated" | "Elinor" | "discontentment" | "foresters" | "refreshments" | "vaguest" | "vices" | "discharge" | "refocusing" | "evangelism" | "builder" | "cryptography" | "adjoins" | "transoceanic" | "chancy" | "rooter" | "tenths" | "chemistry" | "overripe" | "ergo" | "temperature" | "avowing" | "expedites" | "Slovaks" | "Patricia" | "viols" | "covets" | "sauce" | "graveyard" | "almonds" | "dashboards" | "exhalation" | "underlying" | "warranty" | "hideouts" | "landslid" | "flinches" | "cassino" | "mistake" | "stunned" | "dissidents" | "declaimed" | "punts" | "surgery" | "plying" | "spots" | "create" | "teargassed" | "emblematic" | "Auriga" | "tankard" | "intolerant" | "drowsier" | "Charity" | "authoritative" | "sunned" | "rift" | "urges" | "bush" | "zucchinis" | "federate" | "bagged" | "gargoyle" | "ever" | "responds" | "imbibed" | "eating" | "smartening" | "infinities" | "sunbathing" | "maltreated" | "thespian" | "buggier" | "skintight" | "finch" | "philosophies" | "Klondikes" | "picnickers" | "groupies" | "compacting" | "sureness" | "smut" | "censers" | "Huerta" | "motorbike" | "feeblest" | "airy" | "restarting" | "analyzed" | "Compaq" | "curving" | "fifteen" | "kiloton" | "palpitated" | "toasts" | "statue" | "agism" | "baleful" | "honey" | "oozing" | "mattocks" | "manageability" | "programmed" | "hemmed" | "decisiveness" | "crossover" | "growling" | "coiffure" | "explorer" | "flayed" | "arches" | "transaction" | "greyer" | "humiliates" | "vanity" | "rubbery" | "tidbits" | "obeisant" | "believed" | "retrospectively" | "preset" | "harps" | "Vivian" | "wigeon" | "seventeenth" | "geekier" | "tympanums" | "pistons" | "overture" | "soviet" | "bets" | "linearly" | "unwittingly" | "frond" | "Thomistic" | "merit" | "equal" | "bluntly" | "sprites" | "coequals" | "atmospheres" | "slowness" | "depressants" | "engorges" | "tackle" | "nemeses" | "abstainers" | "sager" | "hundredfold" | "skull" | "caterers" | "ministered" | "disinterestedly" | "bunnies" | "rove" | "wino" | "maidenheads" | "vocal" | "bridging" | "engulf" | "bobbies" | "sufficing" | "fruitier" | "skylight" | "auguster" | "rectifying" | "differentiate" | "recipe" | "grading" | "pontiff" | "painful" | "mucks" | "detestation" | "spectacularly" | "Chernenko" | "bearded" | "Rouault" | "butchers" | "calendar" | "forerunner" | "reapportioned" | "perennially" | "wakefulness" | "bawled" | "harpsichord" | "spaded" | "resemblances" | "Orpheus" | "plague" | "planks" | "impalement" | "carolling" | "pubescence" | "housecleans" | "aileron" | "preshrunk" | "tempura" | "tastier" | "eruditely" | "thermals" | "duets" | "squeamishness" | "househusbands" | "Thessalonian" | "spark" | "spearmint" | "horseradish"  // __TO_REPLACE__ 
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
