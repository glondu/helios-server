The Helios-C Election Server
============================

LICENSE: this code is released under the GPL v3 or later.

See QUICKSTART.md for installation instructions.

This is a proof-of-concept implementation of the Helios-C protocol
(pending publication). It is a fork of Ben Adida's Helios Election
Server described [here][1].

[1]: http://heliosvoting.org/


Disclaimer
----------

This code has not been tested extensively and should be used with
care!


Credentials
===========

In Helios-C, each voter has a secret key that is used to sign
ballots. This prevents ballot stuffing.

 * The Schnorr signature scheme is used for signing ballots.
 * The private key is derived from a (relatively) short password
   (advertised as "token" to the voter) that includes a checksum that
   is supposed to be sent to the voter. We estimate that a 15-letter
   password gives 82 of entropy, and this implementation rejects
   shorter ones.
 * The list of authorized public credentials is hard-coded in
   homomorphic.py (authorized_keys) for now.
 * We use the public credential as identity in NIZK proofs. We rely on
   the existing code to implement the revote policy, though, which is
   based on voter objects. In other words, there is no actual check
   that each identity is used only once, as required by the protocol.
   Note that, by design, there need not to be a link between voter
   objects and identities.
 * Ballot auditing needs more work and has been disabled here.


Distributed threshold encryption
================================

This implementation also includes a fully distributed threshold
cryptosystem: only (t+1) out of (l) trustees are needed to perform the
tally. At the moment, t=1 and l=3 are hardcoded in the source code,
but the implementation is generic.

There is now four steps during election setup related to trustees:

 0. Each trustee generates a random that will be presented to him/her
    as a "secret key". From it, setup keypairs (i.e. a signature
    keypair and an encryption keypair) are derived. The trustee then
    upload a self-signed certificate with the public parts to the
    election server.
 1. Each trustee then derives his/her polynomial from the secret
    random, uploads the signed exponentials of its coefficients, and
    the secret shares encrypted with each recipient public key.
 2. Each trustee verifies the secret shares he/she received and
    uploads an acknowledgement.
 3. Each trustee verifies that all acknowledgements are there. It
    means that no complaints has been received. We consider complaints
    to be a social problem and don't address them here.

Each step is a barrier: all trustees must have done step N before any
trustee can do step N+1.

In the implementation, we suppose that all trustees are there for the
tally and we check that all the ways to compute the election result
agree. There is no provision in the user interface for a missing
trustee, so the source code has to be manipulated somehow if some
decryption factors are missing.
