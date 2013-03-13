"""
homomorphic workflow and algorithms for Helios

Ben Adida
2008-08-30
reworked 2011-01-09
"""

import hashlib
import time
from helios.crypto import algs, utils
import logging
import uuid
import datetime
from helios import models
from . import WorkflowObject

logger = logging.getLogger(__name__)

authorized_keys = set ((
    12366106269061813783872003858149335603329148387920798129205999828439916608672741772335863639656158900814926525232453750843248810194199846915030441209646722646220203669819157368783026092481162906907665140512309377194070243010581658493187340643172458840008580365368452136773084917573289325807061996667108268483903995075991206855306838785772327995091181426281791958698012895343480325188258098057589978496427848687403639315920811444073588291830972740147924650652867633619203283243591185853357696389362873837299413336921080678286666885406139749036888887302736819996806029067558346116076351890825700165402519556534614163923, # cTnRU3gXDLrqtzs
    13144886087876098829370314295716147329205838514129460828485386347978171709125049188326045554124152075109960432957728084460183031903937356588574823475160203577224618327270330714222772287322582337779178665209819312260020180730692594546575868063757719928403557853787459938019186006367308880909391367753302095983826334250810086628260314929158515385777426932629247980684459901037531357861274431977337946183575664220553945911147652744684598073486656135716060681992241048197856879173903704174894572659354364266019008651756333924868515992567948183211013551345732789875821965804006881073269714926348157215108389915768483107306, # p7rj9GaFMbCsMiR
    12780779388312207227456323377838619509331043053914036120835986523113500612486572108894825680068855647317315867621966136049766126738704875931709582372078640603979243163760181650678073038464960079159174750941777811352853962758880803080475849909802090200848622222342982203793358348369036336992248873866839715320539461247749693642893841780811660753406981719161692316210337123476254773281698324425246435165851177457337444883611653691986000666606565696824348827389114165044427294873898576802360045470607321407651435406327084530171624410817148462574504594015339456820465514066536531337755084780639242859014574332373946281462, # xdAzSoQx5ZDHZ35
    10038412280524826246150377109336183557795407393395012528754727315418540730198958293137323752183653153871462468200311391085962518980094415133296349413256665255916236048085397967563708590517388801772512171739190121739965005447035931365736943638165043033028403025417845152381834457469783558067516822864109287573358297520492829085512373313480455242158471338602749105188968776590212490362201021101948985376035493765601654752084598979657320999277325522054555748903000422991958768478023827962018090206166064162991331032071257823361989179979683878726728875935602964100437043414622100939810045144715255626711653231267299179917, # GN5HFn4QCine9Wk
    15416531909670900101057012685894748043982332534036164293509932970692766132078770599499470070400270837493121145001325608274301178716621005170659489406775951733476084574632959946004053951908668674246643152670954071613724452871828828157086526860157545187574103793207177838864778253377701986674151989470378158553076938980420675171210733700564748172897777006663474196960991004369642558789632601746514839115713781116482230895709431724504276869736691263536424808203973582244769121368445426321592382863145749449073552604981194166653501881219803201084816708485960852121246997275677176527480759832814136856101154800806451429910, # N9EmFbwxfx4Tvuu
    5775185229671074312533347167693385302160036592921414089453088729222608344329155712282874599265304931401267872184283497802311906425715387401048463161716068854153542204029297088586642566327504717968501643092670855774468328403711956551113148591188058219526633193288946881844199932547992616874965179053212323289621150799497372791994320642472511208072765238873194963844617361665592006848127677888544476752788167550552980686367485189091303455328422503302970420033890215199627759901564588067475961070475717726642827883230146084502313646042537992864876099177302014730675129194798305497240647245009237714611654950350670923008, # ATHZGy2mEGEsp5Z
    13247410048881986831232760155462525965195633633450760651707793395155312523477079147467107684616809497265515685632313998456926699926124515704129779139611302610858532291258010334291024505292685455428250182891407615542497033629306554814771566268471122952565318965068571924219839401186818082484191587743455947257216928536866618951080312727359222959902717201671920664992158415393176761979060011201287826278512301174952774658581306191191973848413756690293042866862814191286576268794185608535938802252303697234562732361801934313351245141332906444594574881123377238990839000302014579602085182400683859024019676709944791431886, # dDxrVZPsUfrYfus
    9246850925466794652984368903172015978810389664474018998581273713854500124842639101642103469234745170180101554551968999789674985143741171061003181855668352506136523327144401400809923757212006217265803023088405881063499297105593073318814422664630153116316216340760283071664891320514526712475048518124202646387509834930823802647284379930092430079728080445188746310052721423857880477082396694996886897812411265220706746295809804864091796077235164677039290321361659107111788113212038403861395828116804634734520112573431631888549852506691910060304328160869607859332697315740250614353504977017758550043931337623546081850575, # WUwWjotAkmtkFAt
    1534182398738340853952347693049887761356045730764395520649396404223800605024026312296880743350442065078218496551484788513920559783839898893011156844186910933708687334526630812995265931751842481539057711011979985686953886226283766276707565098080151490568375437429318440511404731208519963664624274569620179259949292808799831143263295417260202716872092400127314635920635411517542321918206292295053557419450967039054611393454430544023970736306480814369194882102722128502422357976717067300833536600764173113348657361320375333386533248503058055718300471882502352289933978580480260892905813729632892543902590614244702200709, # FAwTaEP7cKxjsxp
    6275174039904243081238442923042258776881108276629089704599681522188448891472941016132232326408319166322763287914090398811456478015505743773196896848620430402196702570470521081078027787946034808284676688017281740824512659258772538395078976346417153306216349059435062333466060592075597064008100910417851160517421221256728189914302184620129721943924154877421971777630380564224934508784693709219735557188966002961533041892705853927776943615114440475598505825250861714009799507448039282582898980806272256478110748699067496581947994070231453490647530371206883246235807328849046167853296619239333967848484314189673644526458, # H8aKYRM6DkHBBgQ
))

class EncryptedAnswer(WorkflowObject):
  """
  An encrypted answer to a single election question
  """

  def __init__(self, choices=None, individual_proofs=None, overall_proof=None, randomness=None, answer=None):
    self.choices = choices
    self.individual_proofs = individual_proofs
    self.overall_proof = overall_proof
    self.randomness = randomness
    self.answer = answer
    
  @classmethod
  def generate_plaintexts(cls, pk, min=0, max=1):
    plaintexts = []
    running_product = 1
    
    # run the product up to the min
    for i in range(max+1):
      # if we're in the range, add it to the array
      if i >= min:
        plaintexts.append(algs.EGPlaintext(running_product, pk))
        
      # next value in running product
      running_product = (running_product * pk.g) % pk.p
      
    return plaintexts

  def verify_plaintexts_and_randomness(self, pk):
    """
    this applies only if the explicit answers and randomness factors are given
    we do not verify the proofs here, that is the verify() method
    """
    if not hasattr(self, 'answer'):
      return False
    
    for choice_num in range(len(self.choices)):
      choice = self.choices[choice_num]
      choice.pk = pk
      
      # redo the encryption
      # WORK HERE (paste from below encryption)
    
    return False
    
  def verify(self, pk, voter_id, min=0, max=1):
    possible_plaintexts = self.generate_plaintexts(pk)
    homomorphic_sum = 0
      
    for choice_num in range(len(self.choices)):
      choice = self.choices[choice_num]
      choice.pk = pk
      individual_proof = self.individual_proofs[choice_num]
      
      # verify the proof on the encryption of that choice
      if not choice.verify_disjunctive_encryption_proof(possible_plaintexts, individual_proof, algs.EG_disjunctive_challenge_generator_with_id(voter_id)):
        return False

      # compute homomorphic sum if needed
      if max != None:
        homomorphic_sum = choice * homomorphic_sum
    
    if max != None:
      # determine possible plaintexts for the sum
      sum_possible_plaintexts = self.generate_plaintexts(pk, min=min, max=max)

      # verify the sum
      return homomorphic_sum.verify_disjunctive_encryption_proof(sum_possible_plaintexts, self.overall_proof, algs.EG_disjunctive_challenge_generator_with_id(voter_id))
    else:
      # approval voting, no need for overall proof verification
      return True
        
  @classmethod
  def fromElectionAndAnswer(cls, election, question_num, answer_indexes):
    """
    Given an election, a question number, and a list of answers to that question
    in the form of an array of 0-based indexes into the answer array,
    produce an EncryptedAnswer that works.
    """
    question = election.questions[question_num]
    answers = question['answers']
    pk = election.public_key
    
    # initialize choices, individual proofs, randomness and overall proof
    choices = [None for a in range(len(answers))]
    individual_proofs = [None for a in range(len(answers))]
    overall_proof = None
    randomness = [None for a in range(len(answers))]
    
    # possible plaintexts [0, 1]
    plaintexts = cls.generate_plaintexts(pk)
    
    # keep track of number of options selected.
    num_selected_answers = 0;
    
    # homomorphic sum of all
    homomorphic_sum = 0
    randomness_sum = 0

    # min and max for number of answers, useful later
    min_answers = 0
    if question.has_key('min'):
      min_answers = question['min']
    max_answers = question['max']

    # go through each possible answer and encrypt either a g^0 or a g^1.
    for answer_num in range(len(answers)):
      plaintext_index = 0
      
      # assuming a list of answers
      if answer_num in answer_indexes:
        plaintext_index = 1
        num_selected_answers += 1

      # randomness and encryption
      randomness[answer_num] = algs.Utils.random_mpz_lt(pk.q)
      choices[answer_num] = pk.encrypt_with_r(plaintexts[plaintext_index], randomness[answer_num])
      
      # generate proof
      individual_proofs[answer_num] = choices[answer_num].generate_disjunctive_encryption_proof(plaintexts, plaintext_index, 
                                                randomness[answer_num], algs.EG_disjunctive_challenge_generator_with_id("FIXME"))
                                                
      # sum things up homomorphically if needed
      if max_answers != None:
        homomorphic_sum = choices[answer_num] * homomorphic_sum
        randomness_sum = (randomness_sum + randomness[answer_num]) % pk.q

    # prove that the sum is 0 or 1 (can be "blank vote" for this answer)
    # num_selected_answers is 0 or 1, which is the index into the plaintext that is actually encoded
    
    if num_selected_answers < min_answers:
      raise Exception("Need to select at least %s answer(s)" % min_answers)
    
    if max_answers != None:
      sum_plaintexts = cls.generate_plaintexts(pk, min=min_answers, max=max_answers)
    
      # need to subtract the min from the offset
      overall_proof = homomorphic_sum.generate_disjunctive_encryption_proof(sum_plaintexts, num_selected_answers - min_answers, randomness_sum, algs.EG_disjunctive_challenge_generator_with_id("FIXME"));
    else:
      # approval voting
      overall_proof = None
    
    return cls(choices, individual_proofs, overall_proof, randomness, answer_indexes)
    
# WORK HERE

class EncryptedVote(WorkflowObject):
  """
  An encrypted ballot
  """
  def __init__(self):
    self.encrypted_answers = None

  @property
  def datatype(self):
    # FIXME
    return "legacy/EncryptedVote"

  def _answers_get(self):
    return self.encrypted_answers

  def _answers_set(self, value):
    self.encrypted_answers = value

  answers = property(_answers_get, _answers_set)

  def verify_signature(self, election):
    pk = election.public_key
    sig = self.signature
    if sig.commitment not in authorized_keys:
      logger.debug("key {0} is not authorized".format(sig.commitment))
      return False
    expected_commitment = (pow(pk.g, sig.response, pk.p) * pow(sig.commitment, sig.challenge, pk.p)) % pk.p
    ea_strings = []
    for ea in self.encrypted_answers:
      ea_choices = []
      for c in ea.choices:
        ea_choices.append(str(c.alpha))
        ea_choices.append(str(c.beta))
      ea_strings.append(",".join(ea_choices))
    string_to_hash = ";".join(ea_strings) + ":" + str(expected_commitment)
    expected_challenge = int(hashlib.sha1(string_to_hash).hexdigest(), 16)
    return expected_challenge == sig.challenge

  def verify(self, election):
    t1 = 1000 * time.clock()
    # right number of answers
    if len(self.encrypted_answers) != len(election.questions):
      return False
    
    # check hash
    if self.election_hash != election.hash:
      # print "%s / %s " % (self.election_hash, election.hash)
      return False
      
    # check ID
    if self.election_uuid != election.uuid:
      return False
      
    # check proofs on all of answers
    for question_num in range(len(election.questions)):
      ea = self.encrypted_answers[question_num]

      question = election.questions[question_num]
      min_answers = 0
      if question.has_key('min'):
        min_answers = question['min']
        
      if not ea.verify(election.public_key, str(self.signature.commitment), min=min_answers, max=question['max']):
        return False
        
    t2 = 1000 * time.clock()
    r = self.verify_signature(election)
    t3 = 1000 * time.clock()
    logger.debug("verify_signature done in {0}, out of {1} ms spent in verify".format(t3-t2, t3-t1))
    return r
    
  @classmethod
  def fromElectionAndAnswers(cls, election, answers):
    pk = election.public_key

    # each answer is an index into the answer array
    encrypted_answers = [EncryptedAnswer.fromElectionAndAnswer(election, answer_num, answers[answer_num]) for answer_num in range(len(answers))]
    return_val = cls()
    return_val.encrypted_answers = encrypted_answers
    return_val.election_hash = election.hash
    return_val.election_uuid = election.uuid

    return return_val
    

class DLogTable(object):
  """
  Keeping track of discrete logs
  """
  
  def __init__(self, base, modulus):
    self.dlogs = {}
    self.dlogs[1] = 0
    self.last_dlog_result = 1
    self.counter = 0
    
    self.base = base
    self.modulus = modulus
    
  def increment(self):
    self.counter += 1
    
    # new value
    new_value = (self.last_dlog_result * self.base) % self.modulus
    
    # record the discrete log
    self.dlogs[new_value] = self.counter
    
    # record the last value
    self.last_dlog_result = new_value
    
  def precompute(self, up_to):
    while self.counter < up_to:
      self.increment()
  
  def lookup(self, value):
    return self.dlogs.get(value, None)
      
    
class Tally(WorkflowObject):
  """
  A running homomorphic tally
  """

  @property
  def datatype(self):
    return "legacy/Tally"
  
  def __init__(self, *args, **kwargs):
    super(Tally, self).__init__()
    
    election = kwargs.get('election',None)
    self.tally = None
    self.num_tallied = 0    

    if election:
      self.init_election(election)
      self.tally = [[0 for a in q['answers']] for q in self.questions]
    else:
      self.questions = None
      self.public_key = None
      self.tally = None

  def init_election(self, election):
    """
    given the election, initialize some params
    """
    self.election = election
    self.questions = election.questions
    self.public_key = election.public_key
    
  def add_vote_batch(self, encrypted_votes, verify_p=True):
    """
    Add a batch of votes. Eventually, this will be optimized to do an aggregate proof verification
    rather than a whole proof verif for each vote.
    """
    for vote in encrypted_votes:
      self.add_vote(vote, verify_p)
    
  def add_vote(self, encrypted_vote, verify_p=True):
    # do we verify?
    if verify_p:
      if not encrypted_vote.verify(self.election):
        raise Exception('Bad Vote')

    # for each question
    for question_num in range(len(self.questions)):
      question = self.questions[question_num]
      answers = question['answers']
      
      # for each possible answer to each question
      for answer_num in range(len(answers)):
        # do the homomorphic addition into the tally
        enc_vote_choice = encrypted_vote.encrypted_answers[question_num].choices[answer_num]
        enc_vote_choice.pk = self.public_key
        self.tally[question_num][answer_num] = encrypted_vote.encrypted_answers[question_num].choices[answer_num] * self.tally[question_num][answer_num]

    self.num_tallied += 1

  def decryption_factors_and_proofs(self, sk):
    """
    returns an array of decryption factors and a corresponding array of decryption proofs.
    makes the decryption factors into strings, for general Helios / JS compatibility.
    """
    # for all choices of all questions (double list comprehension)
    decryption_factors = []
    decryption_proof = []
    
    for question_num, question in enumerate(self.questions):
      answers = question['answers']
      question_factors = []
      question_proof = []

      for answer_num, answer in enumerate(answers):
        # do decryption and proof of it
        dec_factor, proof = sk.decryption_factor_and_proof(self.tally[question_num][answer_num])

        # look up appropriate discrete log
        # this is the string conversion
        question_factors.append(dec_factor)
        question_proof.append(proof)
        
      decryption_factors.append(question_factors)
      decryption_proof.append(question_proof)
    
    return decryption_factors, decryption_proof
    
  def decrypt_and_prove(self, sk, discrete_logs=None):
    """
    returns an array of tallies and a corresponding array of decryption proofs.
    """
    
    # who's keeping track of discrete logs?
    if not discrete_logs:
      discrete_logs = self.discrete_logs
      
    # for all choices of all questions (double list comprehension)
    decrypted_tally = []
    decryption_proof = []
    
    for question_num in range(len(self.questions)):
      question = self.questions[question_num]
      answers = question['answers']
      question_tally = []
      question_proof = []

      for answer_num in range(len(answers)):
        # do decryption and proof of it
        plaintext, proof = sk.prove_decryption(self.tally[question_num][answer_num])

        # look up appropriate discrete log
        question_tally.append(discrete_logs[plaintext])
        question_proof.append(proof)
        
      decrypted_tally.append(question_tally)
      decryption_proof.append(question_proof)
    
    return decrypted_tally, decryption_proof
  
  def verify_decryption_proofs(self, decryption_factors, decryption_proofs, public_key, challenge_generator):
    """
    decryption_factors is a list of lists of dec factors
    decryption_proofs are the corresponding proofs
    public_key is, of course, the public key of the trustee
    """

    # go through each one
    for q_num, q in enumerate(self.tally):
      for a_num, answer_tally in enumerate(q):
        # parse the proof
        #proof = algs.EGZKProof.fromJSONDict(decryption_proofs[q_num][a_num])
        proof = decryption_proofs[q_num][a_num]
        
        # check that g, alpha, y, dec_factor is a DH tuple
        if not proof.verify(public_key.g, answer_tally.alpha, public_key.y, int(decryption_factors[q_num][a_num]), public_key.p, public_key.q, challenge_generator):
          return False
    
    return True
    
  def decrypt_from_factors(self, decryption_factors, public_key):
    """
    decrypt a tally given decryption factors
    
    The decryption factors are a list of decryption factor sets, for each trustee.
    Each decryption factor set is a list of lists of decryption factors (questions/answers).
    """
    
    # pre-compute a dlog table
    dlog_table = DLogTable(base = public_key.g, modulus = public_key.p)
    dlog_table.precompute(self.num_tallied)
    
    result = []
    
    # go through each one
    for q_num, q in enumerate(self.tally):
      q_result = []

      for a_num, a in enumerate(q):
        # coalesce the decryption factors into one list
        dec_factor_list = [df[q_num][a_num] for df in decryption_factors]
        raw_value = self.tally[q_num][a_num].decrypt(dec_factor_list, public_key)
        
        q_result.append(dlog_table.lookup(raw_value))

      result.append(q_result)
    
    return result

  def _process_value_in(self, field_name, field_value):
    if field_name == 'tally':
      return [[algs.EGCiphertext.fromJSONDict(a) for a in q] for q in field_value]
      
  def _process_value_out(self, field_name, field_value):
    if field_name == 'tally':
      return [[a.toJSONDict() for a in q] for q in field_value]    
        
