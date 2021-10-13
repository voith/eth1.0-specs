"""
Ethereum Virtual Machine (EVM) Block Instructions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Implementations of the EVM block instructions.
"""

from ethereum.base_types import U256

from .. import Evm
from ..gas import GAS_BASE, GAS_EXTERNAL, subtract_gas
from ..stack import pop, push


def block_hash(evm: Evm) -> None:
    """
    Push the hash of one of the 256 most recent complete blocks onto the
    stack. The block number to hash is present at the top of the stack.

    Parameters
    ----------
    evm :
        The current EVM frame.

    Raises
    ------
    StackUnderflowError
        If `len(stack)` is less than `1`.
    OutOfGasError
        If `evm.gas_left` is less than `20`.
    """
    evm.gas_left = subtract_gas(evm.gas_left, GAS_EXTERNAL)

    block_number = pop(evm.stack)

    is_ancestor_depth_out_of_range = (
        evm.env.number < block_number + 1
        or evm.env.number - block_number - 1 >= 256
        or evm.env.number - block_number - 1 < 0
    )

    if is_ancestor_depth_out_of_range:
        _hash = b"\x00"
    else:
        try:
            _hash = evm.env.block_hashes[evm.env.number - block_number - 1]
        except IndexError:
            # Ancestor with specified depth not present
            _hash = b"\x00"

    push(evm.stack, U256.from_be_bytes(_hash))

    evm.pc += 1


def coinbase(evm: Evm) -> None:
    """
    Push the current block's beneficiary address (address of the block miner)
    onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    evm :
        The current EVM frame.

    Raises
    ------
    StackOverflowError
        If `len(stack)` is equal to `1024`.
    OutOfGasError
        If `evm.gas_left` is less than `2`.
    """
    evm.gas_left = subtract_gas(evm.gas_left, GAS_BASE)
    push(evm.stack, U256.from_be_bytes(evm.env.coinbase))

    evm.pc += 1


def timestamp(evm: Evm) -> None:
    """
    Push the current block's timestamp onto the stack. Here the timestamp
    being referred is actually the unix timestamp in seconds.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    evm :
        The current EVM frame.

    Raises
    ------
    StackOverflowError
        If `len(stack)` is equal to `1024`.
    OutOfGasError
        If `evm.gas_left` is less than `2`.
    """
    evm.gas_left = subtract_gas(evm.gas_left, GAS_BASE)
    push(evm.stack, evm.env.time)

    evm.pc += 1


def number(evm: Evm) -> None:
    """
    Push the current block's number onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    evm :
        The current EVM frame.

    Raises
    ------
    StackOverflowError
        If `len(stack)` is equal to `1024`.
    OutOfGasError
        If `evm.gas_left` is less than `2`.
    """
    evm.gas_left = subtract_gas(evm.gas_left, GAS_BASE)
    push(evm.stack, U256(evm.env.number))

    evm.pc += 1


def difficulty(evm: Evm) -> None:
    """
    Push the current block's difficulty onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    evm :
        The current EVM frame.

    Raises
    ------
    StackOverflowError
        If `len(stack)` is equal to `1024`.
    OutOfGasError
        If `evm.gas_left` is less than `2`.
    """
    evm.gas_left = subtract_gas(evm.gas_left, GAS_BASE)
    push(evm.stack, U256(evm.env.difficulty))

    evm.pc += 1


def gas_limit(evm: Evm) -> None:
    """
    Push the current block's gas limit onto the stack.

    Here the current block refers to the block in which the currently
    executing transaction/call resides.

    Parameters
    ----------
    evm :
        The current EVM frame.

    Raises
    ------
    StackOverflowError
        If `len(stack)` is equal to `1024`.
    OutOfGasError
        If `evm.gas_left` is less than `2`.
    """
    evm.gas_left = subtract_gas(evm.gas_left, GAS_BASE)
    push(evm.stack, U256(evm.env.gas_limit))

    evm.pc += 1
