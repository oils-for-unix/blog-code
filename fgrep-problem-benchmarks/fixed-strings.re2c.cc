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

      "crackle" | "maturest" | "Rumania" | "diverged" | "accommodating" | "contracting" | "sweeten" | "improving" | "nasalizing" | "harangue" | "citrous" | "surtax" | "Indra" | "Sundas" | "topic" | "zonked" | "continentals" | "shares" | "serenity" | "carryall" | "hove" | "gray" | "exclaim" | "pickings" | "Seiko" | "foreshortening" | "verier" | "preconceived" | "tossed" | "pincers" | "fizzes" | "warfare" | "bisections" | "distance" | "cloudburst" | "humanizes" | "beaten" | "gnaw" | "Donizetti" | "obtruding" | "slot" | "autopsied" | "desperadoes" | "clucking" | "analgesic" | "nation" | "mower" | "mergansers" | "counteracting" | "skywriting" | "oversee" | "malapropisms" | "woodcarving" | "clampdown" | "sterilization" | "unbutton" | "coaching" | "worryings" | "impresses" | "madcaps" | "groomed" | "gratuities" | "caraway" | "leaf" | "demo" | "waterier" | "spraining" | "deriving" | "puniest" | "poverty" | "alcohols" | "fabulously" | "pettier" | "weeknights" | "interlock" | "Garland" | "redeploys" | "spectroscopic" | "competency" | "staffing" | "govern" | "fireworks" | "Onassis" | "prefect" | "Czechs" | "pocket" | "Roach" | "Xmas" | "wordings" | "conundrum" | "enthrones" | "loanwords" | "crudest" | "Sallust" | "salvaged" | "stringent" | "bassoonist" | "percolated" | "Oort" | "baffles" | "strenuous" | "reclined" | "miserable" | "Scarlatti" | "aphelions" | "aquaplane" | "unions" | "Spenglerian" | "Lynnette" | "wallowing" | "greenhouses" | "counseling" | "Occidentals" | "moisturize" | "indifferent" | "charting" | "wardens" | "exacerbates" | "fulcra" | "narked" | "profiling" | "estimates" | "although" | "monthlies" | "treacherous" | "Ashikaga" | "Delphinus" | "insufficient" | "Hermitage" | "absolutes" | "Eugene" | "mambo" | "mulled" | "witnesses" | "carnations" | "Freon" | "Orbison" | "thoughtlessness" | "perturbing" | "sled" | "yams" | "yelping" | "Styron" | "snuggled" | "epidermises" | "acknowledgments" | "coaches" | "evaporates" | "withstands" | "hammerhead" | "commutes" | "initialling" | "tyrannosaurus" | "audibly" | "mistreatment" | "transistor" | "disloyal" | "colloquialism" | "baffling" | "Wassermann" | "laughably" | "gelded" | "humbled" | "extravert" | "sadist" | "eliciting" | "bludgeoned" | "fare" | "leave" | "adverts" | "reductions" | "lumberjacks" | "racially" | "believe" | "mononucleosis" | "flickers" | "applicator" | "unkindest" | "policeman" | "preempted" | "beholding" | "jocose" | "Blaine" | "transfixt" | "storyteller" | "Finch" | "descendant" | "detaches" | "snaps" | "weal" | "phonemic" | "desiccate" | "salamanders" | "encored" | "schrod" | "waltz" | "maxed" | "repentant" | "frailties" | "carpetbaggers" | "narc" | "leukocyte" | "laughed" | "rakishly" | "coldness" | "permafrost" | "Marquesas" | "unimpressed" | "liquor" | "baring" | "category" | "stigmatizing" | "anesthesia" | "brayed" | "sync" | "Indore" | "surfboard" | "feelers" | "raucous" | "Jerrod" | "internally" | "trundle" | "bluster" | "deport" | "unsettle" | "Goethals" | "Billings" | "woodland" | "case" | "ranch" | "catalepsy" | "Erin" | "vapor" | "Brooke" | "encircles" | "crinolines" | "wholeness" | "petrel" | "Assyria" | "phenotype" | "radiologists" | "prequel" | "Rocco" | "promotional" | "Tiffany" | "sulkily" | "markedly" | "costar" | "intercepts" | "barbiturates" | "shoed" | "survive" | "aeons" | "empties" | "urinal" | "Enkidu" | "brief" | "foreclose" | "Dior" | "ridging" | "victim" | "expected" | "shenanigan" | "advising" | "Esperanza" | "trafficking" | "emaciate" | "ruminants" | "suctioning" | "looting" | "booting" | "herculean" | "inadvisable" | "meanings" | "bewilders" | "longest" | "gasohol" | "survivors" | "commutative" | "understated" | "destining" | "irresponsible" | "technologically" | "Vazquez" | "penes" | "quicksilver" | "regionally" | "boutique" | "punctures" | "Lesley" | "sounds" | "glens" | "Clouseau" | "visibly" | "untruth" | "authoritarian" | "quixotic" | "upstarts" | "pimping" | "riced" | "smallness" | "sapping" | "cognate" | "teazels" | "spottiest" | "overeating" | "rajahs" | "cares" | "ovoids" | "Franz" | "longshoreman" | "mumbling" | "identify" | "harmonizes" | "aggravates" | "impious" | "hulled" | "gamy" | "stinks" | "tempts" | "Ruskin" | "bondage" | "Hoover" | "aficionado" | "Lyman" | "thinnest" | "fleeces" | "hanged" | "tills" | "microfilmed" | "celebration" | "enrich" | "Senate" | "entrap" | "Gloucester" | "Guatemala" | "abuse" | "Couperin" | "squeegee" | "Algonquian" | "bible" | "favors" | "bummers" | "hydrants" | "parallel" | "brimful" | "Oregon" | "super" | "wainscot" | "baptistries" | "scuffles" | "quavering" | "rooftop" | "popinjay" | "finessed" | "burly" | "Lochinvar" | "horribly" | "poised" | "bygones" | "seacoast" | "resurgences" | "tripped" | "Narnia" | "hokey" | "wavier" | "unpunished" | "algorithm" | "infinities" | "mulls" | "lyrics" | "puttering" | "heightened" | "Cliburn" | "envied" | "trills" | "strengthen" | "pacifiers" | "Marty" | "tortuous" | "witchcraft" | "Marsh" | "interrupts" | "cryptography" | "Forester" | "harshly" | "scratchiest" | "hysterectomy" | "proposition" | "hydra" | "Nikolayev" | "verdant" | "drugs" | "freshen" | "abomination" | "prejudge" | "hesitantly" | "undetected" | "windsock" | "Alabaman"  // __TO_REPLACE__ 
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
